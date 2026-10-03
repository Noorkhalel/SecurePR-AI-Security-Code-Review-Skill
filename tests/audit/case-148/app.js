export function leave(req, res) {
  const routes = new Map([['home', '/home'], ['account', '/account']]);
  const destination = routes.get(req.query.next);
  if (!destination) return res.sendStatus(400);
  return res.redirect(destination);
}
