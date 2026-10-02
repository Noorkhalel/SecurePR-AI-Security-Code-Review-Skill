import jwt from 'jsonwebtoken';
export function register(app, users) {
  app.get('/me', async (req, res) => {
    const token = req.headers.authorization?.slice(7);
    const claims = jwt.decode(token);
    if (!claims?.sub) return res.status(401).end();
    res.json(await users.findById(claims.sub));
  });
}
