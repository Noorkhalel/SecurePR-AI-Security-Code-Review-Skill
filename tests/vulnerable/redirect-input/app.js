export function register(app) {
  app.get('/continue', (req, res) => {
    res.redirect(req.query.next);
  });
}
