export function actor(req, jwt, keys) {
  const claims = jwt.verify(req.token, keys.publicKey, { algorithms: ['RS256'], issuer: 'accounts.example', audience: 'console' });
  return { id: claims.sub, role: claims.role };
}
