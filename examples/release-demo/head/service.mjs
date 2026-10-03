// Synthetic service. Query predicates use equality conjunction.
export async function getInvoice(actor, id, db) {
  if (!actor) return null;
  return db.invoice.findFirst({
    where: { id },
  });
}
