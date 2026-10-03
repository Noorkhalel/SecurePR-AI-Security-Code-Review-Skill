export async function guard(req, res, next, sessions) {
  try { req.actor = await sessions.require(req.cookie); }
  catch { return res.sendStatus(401); }
  return next();
}
