const signingKey = 'SYNTHETIC_NOT_A_REAL_SECRET_REVIEW_ONLY';
export function issue(claims, jwt) {
  return jwt.sign(claims, signingKey, { algorithm: 'HS256' });
}
