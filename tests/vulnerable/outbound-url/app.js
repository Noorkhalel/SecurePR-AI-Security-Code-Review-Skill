export function register(app) {
  app.post('/preview', async (req, res) => {
    const response = await fetch(req.body.url);
    res.type('text').send(await response.text());
  });
}
