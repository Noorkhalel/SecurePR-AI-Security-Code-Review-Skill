// Trusted synthetic release demo. No listener, dependencies or external services.
// Generated test assertions with release-maintainer adapters for actual demo modules.
// This is not an Express or database integration test.
import test from 'node:test';
import assert from 'node:assert/strict';
const mode = process.env.SECUREPR_TEST_VARIANT ?? 'after';
assert.ok(['before', 'after'].includes(mode), 'SECUREPR_TEST_VARIANT must be before or after');
const { getInvoice } = mode === 'before'
  ? await import('./head/service.mjs') : await import('./fixed/service.mjs');
const { mountInvoiceRoutes } = mode === 'before'
  ? await import('./head/routes.mjs') : await import('./fixed/routes.mjs');
const actor = Object.freeze({ id: 'owner-a', tenantId: 'tenant-a' });

function makeStore() {
  const rows = [
    { id: 'own-invoice', ownerId: 'owner-a', tenantId: 'tenant-a', total: 120 },
    { id: 'other-owner', ownerId: 'owner-b', tenantId: 'tenant-a', total: 230 },
    { id: 'other-tenant', ownerId: 'owner-a', tenantId: 'tenant-b', total: 340 },
    { id: 'other-both', ownerId: 'owner-b', tenantId: 'tenant-b', total: 450 },
  ];
  const original = structuredClone(rows);
  let calls = 0;
  const db = {
    invoice: {
      async findFirst({ where }) {
        calls += 1;
        const hit = rows.find(row => Object.entries(where).every(
          ([key, value]) => Object.hasOwn(row, key) && row[key] === value,
        ));
        return hit ? structuredClone(hit) : null;
      },
    },
  };
  return { db, rows, original, calls: () => calls };
}

// Execute the registered synthetic handler with in-memory request/response and
// session adapters. Session integrity is a supplied contract, not tested auth.
async function responseFor(session, id, db) {
  let registration;
  const app = { get(path, guard, handler) {
    assert.equal(registration, undefined, 'one route registration');
    assert.equal(path, '/api/invoices/:id');
    registration = { guard, handler };
  } };
  function requireSession(req, res, next) {
    if (!session || !session.valid) return res.status(401).json({ error: 'Unauthorized' });
    req.user = session.user;
    return next();
  }
  mountInvoiceRoutes(app, { requireSession, db });
  const result = { status: 200 };
  const res = { status(code) { result.status = code; return this; },
    json(body) { result.body = body; return result; } };
  const req = { params: { id } };
  await registration.guard(req, res, () => registration.handler(req, res, error => { throw error; }));
  return result;
}
const validSession = Object.freeze({ valid: true, user: actor });

test(`${mode}: owner in correct tenant receives intended invoice`, async () => {
  const store = makeStore();
  assert.deepEqual(await responseFor(validSession, 'own-invoice', store.db), {
    status: 200, body: { id: 'own-invoice', total: 120 },
  });
  assert.equal(store.calls(), 1);
  assert.deepEqual(store.rows, store.original);
});

for (const [label, id] of [
  ['different owner in same tenant', 'other-owner'],
  ['same owner in different tenant', 'other-tenant'],
  ['different owner and tenant', 'other-both'],
]) {
  test(`${mode}: deny ${label} without disclosure or mutation`, async () => {
    const store = makeStore();
    const response = await responseFor(validSession, id, store.db);
    assert.deepEqual(store.rows, store.original);
    assert.deepEqual(response, { status: 404, body: { error: 'Not found' } });
    assert.equal(Object.hasOwn(response.body, 'id'), false);
    assert.equal(Object.hasOwn(response.body, 'total'), false);
  });
}

test(`${mode}: unknown invoice has identical non-disclosing denial`, async () => {
  const store = makeStore();
  assert.deepEqual(await responseFor(validSession, 'absent-invoice', store.db), {
    status: 404, body: { error: 'Not found' },
  });
  assert.deepEqual(store.rows, store.original);
});

for (const [label, session] of [
  ['absent session', null],
  ['invalid session', { valid: false, user: actor }],
]) {
  test(`${mode}: ${label} stops before database access`, async () => {
    const store = makeStore();
    assert.deepEqual(await responseFor(session, 'own-invoice', store.db), {
      status: 401, body: { error: 'Unauthorized' },
    });
    assert.equal(store.calls(), 0);
    assert.deepEqual(store.rows, store.original);
  });
}

test(`${mode}: absent service actor returns null without database access`, async () => {
  const store = makeStore();
  assert.equal(await getInvoice(null, 'own-invoice', store.db), null);
  assert.equal(store.calls(), 0);
  assert.deepEqual(store.rows, store.original);
});
