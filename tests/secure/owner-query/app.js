export function register(app, requireSession, db) {
  app.get('/invoices/:id', requireSession, async (req, res) => {
    const invoice = await db.invoice.findFirst({ where: { id: req.params.id, ownerId: req.user.id, tenantId: req.user.tenantId } });
    if (!invoice) return res.status(404).end();
    res.json(invoice);
  });
}
