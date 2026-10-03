export function exportDocs(req, db) {
  return db.document.findMany({ where: { id: { in: req.body.ids }, tenantId: req.actor.tenantId } });
}
