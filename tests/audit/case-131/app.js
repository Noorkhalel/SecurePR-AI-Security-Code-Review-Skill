export function createDoc(req, db) {
  return db.document.create({ data: { title: req.body.title, tenantId: req.actor.tenantId } });
}
