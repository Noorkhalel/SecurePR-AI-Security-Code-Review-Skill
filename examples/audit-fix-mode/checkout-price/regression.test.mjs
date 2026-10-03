import test from 'node:test';
import assert from 'node:assert/strict';

const variant = process.env.SECUREPR_TEST_VARIANT ?? 'after';
if (variant !== 'before' && variant !== 'after') throw new Error('Invalid test variant');
const { checkout } = variant === 'before'
  ? await import('./before.mjs') : await import('./after.mjs');

function fixture() {
  const actor = { id: 'buyer-a', tenantId: 'shop-a' };
  const carts = [{
    id: 'cart-a', ownerId: 'buyer-a', tenantId: 'shop-a',
    state: 'open', totalCents: 4200, currency: 'USD',
  }];
  const receipts = [];
  // Storage only: this fake accepts any supplied receipt amount.
  const store = {
    get(id) { return structuredClone(carts.find(cart => cart.id === id)); },
    complete(id, receipt) {
      carts.find(cart => cart.id === id).state = 'completed';
      receipts.push(structuredClone(receipt));
    },
  };
  return { actor, carts, receipts, store };
}

test('the owner checks out an open cart at its server quote', () => {
  const f = fixture();
  const originalActor = structuredClone(f.actor);
  assert.deepEqual(checkout(f.actor, 'cart-a', {}, f.store), { status: 201 });
  assert.deepEqual(f.receipts, [{ cartId: 'cart-a', totalCents: 4200, currency: 'USD' }]);
  assert.deepEqual(f.carts, [{
    id: 'cart-a', ownerId: 'buyer-a', tenantId: 'shop-a',
    state: 'completed', totalCents: 4200, currency: 'USD',
  }]);
  assert.deepEqual(f.actor, originalActor);
});

test('a client amount cannot change the charged amount or the stored quote', () => {
  const f = fixture();
  assert.deepEqual(checkout(f.actor, 'cart-a', { totalCents: 1 }, f.store), { status: 201 });
  assert.deepEqual(f.receipts, [{ cartId: 'cart-a', totalCents: 4200, currency: 'USD' }]);
  assert.equal(f.carts[0].totalCents, 4200);
  assert.equal(f.carts[0].state, 'completed');
});

for (const [label, actor, cartId] of [
  ['another owner', { id: 'buyer-b', tenantId: 'shop-a' }, 'cart-a'],
  ['another tenant', { id: 'buyer-a', tenantId: 'shop-b' }, 'cart-a'],
  ['missing cart', { id: 'buyer-a', tenantId: 'shop-a' }, 'missing'],
]) {
  test(`${label} is denied without an order or cart change`, () => {
    const f = fixture();
    const original = structuredClone(f.carts);
    assert.deepEqual(checkout(actor, cartId, {}, f.store), { status: 404 });
    assert.deepEqual(f.carts, original);
    assert.deepEqual(f.receipts, []);
  });
}

test('an unauthenticated caller cannot reach storage', () => {
  const store = { get() { assert.fail('unexpected storage access'); } };
  assert.deepEqual(checkout(null, 'cart-a', {}, store), { status: 401 });
});

test('a sequential repeat cannot create a second order or change state', () => {
  const f = fixture();
  assert.deepEqual(checkout(f.actor, 'cart-a', {}, f.store), { status: 201 });
  const completed = structuredClone({ carts: f.carts, receipts: f.receipts });
  assert.deepEqual(checkout(f.actor, 'cart-a', {}, f.store), { status: 409 });
  assert.deepEqual({ carts: f.carts, receipts: f.receipts }, completed);
});

test('an invalid server quote cannot be replaced by a client amount', () => {
  const f = fixture();
  f.carts[0].totalCents = 0;
  const original = structuredClone(f.carts);
  const result = checkout(f.actor, 'cart-a', { totalCents: 4200 }, f.store);
  assert.deepEqual(f.carts, original, 'invalid quote must not complete the cart');
  assert.deepEqual(f.receipts, [], 'invalid quote must not create a receipt');
  assert.deepEqual(result, { status: 422 });
});
