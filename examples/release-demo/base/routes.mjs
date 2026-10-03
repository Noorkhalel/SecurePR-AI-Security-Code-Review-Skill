// Synthetic Express-compatible route; never deployed.
import { getInvoice } from './service.mjs';
export function mountInvoiceRoutes(app, { requireSession, db }) {
  app.get('/api/invoices/:id', requireSession, async (req, res, next) => {
    try {
      const invoice = await getInvoice(req.user, req.params.id, db);
      if (!invoice) return res.status(404).json({ error: 'Not found' });
      return res.json({ id: invoice.id, total: invoice.total });
    } catch (error) {
      return next(error);
    }
  });
}
