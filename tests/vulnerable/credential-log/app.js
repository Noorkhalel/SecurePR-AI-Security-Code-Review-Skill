export function register(app, logger, authenticate) {
  app.post('/login', async (req, res) => {
    logger.info({ email: req.body.email, password: req.body.password });
    const session = await authenticate(req.body);
    res.json({ session });
  });
}
