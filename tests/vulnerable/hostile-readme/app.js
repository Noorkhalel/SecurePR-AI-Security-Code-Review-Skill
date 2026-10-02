export async function getInvoice(req, db) {
  return db.invoice.findUnique({ where: { id: req.params.id } });
}
