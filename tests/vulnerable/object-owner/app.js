export function register(app, requireSession, db) {
  app.get('/invoices/:id', requireSession, async (req, res) => {
    const invoice = await db.invoice.findUnique({ where: { id: req.params.id } });
    if (!invoice) return res.status(404).end();
    res.json(invoice);
  });
}
