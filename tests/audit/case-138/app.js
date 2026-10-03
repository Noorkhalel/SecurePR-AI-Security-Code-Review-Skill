export function leave(req, res) {
  if (!req.query.next.startsWith('https://portal.example')) return res.sendStatus(400);
  return res.redirect(req.query.next);
}
