export function issue(claims, jwt, provisioned) {
  return jwt.sign(claims, provisioned.signingKey, { algorithm: 'HS256' });
}
