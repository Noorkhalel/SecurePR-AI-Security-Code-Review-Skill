// Trusted synthetic regression demonstration; execution results are in EVALUATION.md.
import test from 'node:test';
import assert from 'node:assert/strict';

const variant = process.env.SECUREPR_TEST_VARIANT ?? 'after';
if (variant !== 'before' && variant !== 'after') {
  throw new Error('SECUREPR_TEST_VARIANT must be before or after');
}
// Literal module paths prevent environment-controlled arbitrary imports.
const { getInvoice } = variant === 'before'
  ? await import('./before.mjs')
  : await import('./after.mjs');

function fixture() {
  const actor = { id: 'owner-a', tenantId: 'tenant-a' };
  const records = [
    { id: 'invoice-own', ownerId: 'owner-a', tenantId: 'tenant-a', total: 100 },
    { id: 'invoice-other-owner', ownerId: 'owner-b', tenantId: 'tenant-a', total: 200 },
    { id: 'invoice-other-tenant', ownerId: 'owner-a', tenantId: 'tenant-b', total: 300 },
  ];
  const db = {
    invoice: {
      async findFirst({ where }) {
        // This tiny adapter models equality conjunction, not authorization policy.
        return records.find(row => Object.entries(where).every(
          ([field, value]) => row[field] === value,
        )) ?? null;
      },
    },
  };
  return { actor, records, db };
}

const cases = [
  { name: 'authorized owner in matching tenant receives the invoice', id: 'invoice-own', allowed: true },
  { name: 'another owner in the same tenant is denied', id: 'invoice-other-owner' },
  { name: 'same owner in another tenant is denied', id: 'invoice-other-tenant' },
  { name: 'a missing invoice returns null', id: 'invoice-missing' },
  { name: 'an unauthenticated caller is denied', id: 'invoice-own', unauthenticated: true },
];

for (const scenario of cases) {
  test(`${scenario.name}; records and actor remain unchanged`, async () => {
    const { actor, records, db } = fixture();
    const originalRecords = structuredClone(records);
    const originalActor = structuredClone(actor);
    const result = await getInvoice(scenario.unauthenticated ? null : actor, scenario.id, db);
    assert.deepEqual(records, originalRecords, 'must not mutate any invoice');
    assert.deepEqual(actor, originalActor, 'must not mutate session identity');
    assert.deepEqual(result, scenario.allowed ? originalRecords[0] : null);
  });
}

test('unauthenticated callers do not access the database', async () => {
  const db = { invoice: { findFirst() { assert.fail('unexpected database access'); } } };
  assert.equal(await getInvoice(null, 'invoice-own', db), null);
});
