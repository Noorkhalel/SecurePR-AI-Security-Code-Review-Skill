export function actor(req, jwt, keys) {
  const claims = jwt.decode(req.token);
  return { id: claims.sub, role: claims.role };
}
