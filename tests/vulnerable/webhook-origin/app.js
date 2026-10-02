export function register(app, orders) {
  app.post('/provider-events', async (req, res) => {
    if (req.body.type === 'payment.succeeded') {
      await orders.markPaid(req.body.orderId);
    }
    res.status(204).end();
  });
}
