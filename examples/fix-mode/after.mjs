// Synthetic regression demonstration. No server, credentials or external services.
export async function getInvoice(actor, id, db) {
  if (!actor) return null;
  return db.invoice.findFirst({
    where: { id, ownerId: actor.id, tenantId: actor.tenantId },
  });
}
