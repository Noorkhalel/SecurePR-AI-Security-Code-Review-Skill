export function createDoc(req, db) {
  return db.document.create({ data: { tenantId: req.actor.tenantId, ...req.body } });
}
