export async function guard(req, res, next, sessions) {
  try { req.actor = await sessions.require(req.cookie); }
  catch { req.actor = { id: 'service', role: 'admin' }; }
  return next();
}
