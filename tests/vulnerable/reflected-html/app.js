export function register(app) {
  app.get('/greeting', (req, res) => {
    res.type('html').send(`<p>Hello ${req.query.name}</p>`);
  });
}
