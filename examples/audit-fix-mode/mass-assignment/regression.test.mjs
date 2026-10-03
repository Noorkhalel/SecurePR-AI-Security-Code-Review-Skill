import test from 'node:test';
import assert from 'node:assert/strict';

const variant = process.env.SECUREPR_TEST_VARIANT ?? 'after';
if (variant !== 'before' && variant !== 'after') throw new Error('Invalid test variant');
const { updateProfile } = variant === 'before'
  ? await import('./before.mjs') : await import('./after.mjs');

function fixture() {
  const actor = { id: 'member-a', tenantId: 'team-a' };
  const records = [{
    id: 'profile-a', ownerId: 'member-a', tenantId: 'team-a',
    displayName: 'Original name', role: 'member', creditCents: 1200,
  }];
  let writes = 0;
  // Storage only: no field policy or authorization is implemented in this fake.
  const store = {
    get(id) { return structuredClone(records.find(record => record.id === id)); },
    replace(id, replacement) {
      const index = records.findIndex(record => record.id === id);
      if (index < 0) throw new Error('Record missing');
      records[index] = structuredClone(replacement);
      writes += 1;
    },
  };
  return { actor, records, store, writes: () => writes };
}

test('a member updates their display name and preserves server fields', () => {
  const f = fixture();
  const originalActor = structuredClone(f.actor);
  assert.deepEqual(updateProfile(f.actor, 'profile-a', { displayName: 'New name' }, f.store), { status: 204 });
  assert.deepEqual(f.records, [{
    id: 'profile-a', ownerId: 'member-a', tenantId: 'team-a',
    displayName: 'New name', role: 'member', creditCents: 1200,
  }]);
  assert.equal(f.writes(), 1);
  assert.deepEqual(f.actor, originalActor);
});

for (const [field, value] of [
  ['role', 'administrator'], ['tenantId', 'team-b'], ['creditCents', 9000],
]) {
  test(`a request containing protected ${field} is rejected without a partial update`, () => {
    const f = fixture();
    const original = structuredClone(f.records);
    const result = updateProfile(f.actor, 'profile-a', { displayName: 'New name', [field]: value }, f.store);
    assert.deepEqual(f.records, original, 'all persistent fields must remain unchanged');
    assert.equal(f.writes(), 0, 'denied input must cause no storage writes');
    assert.deepEqual(result, { status: 422 });
  });
}

for (const [label, actor, profileId, status] of [
  ['another owner', { id: 'member-b', tenantId: 'team-a' }, 'profile-a', 404],
  ['another tenant', { id: 'member-a', tenantId: 'team-b' }, 'profile-a', 404],
  ['missing profile', { id: 'member-a', tenantId: 'team-a' }, 'missing', 404],
]) {
  test(`${label} cannot modify the profile`, () => {
    const f = fixture();
    const original = structuredClone(f.records);
    assert.deepEqual(updateProfile(actor, profileId, { displayName: 'New name' }, f.store), { status });
    assert.deepEqual(f.records, original);
    assert.equal(f.writes(), 0);
  });
}

test('an unauthenticated caller cannot reach storage', () => {
  const store = { get() { assert.fail('unexpected storage access'); } };
  assert.deepEqual(updateProfile(null, 'profile-a', { displayName: 'New name' }, store), { status: 401 });
});

test('invalid display name is rejected without mutation', () => {
  const f = fixture();
  const original = structuredClone(f.records);
  assert.deepEqual(updateProfile(f.actor, 'profile-a', { displayName: ' ' }, f.store), { status: 422 });
  assert.deepEqual(f.records, original);
  assert.equal(f.writes(), 0);
});
