// Output-only correction for HIGH-01 in the task-supplied synthetic model.
// The task contract provides validated, server-derived actor identity.
export async function getInvoice(actor, id, db) {
  if (!actor) return null;
  return db.invoice.findFirst({
    where: { id, ownerId: actor.id, tenantId: actor.tenantId },
  });
}
