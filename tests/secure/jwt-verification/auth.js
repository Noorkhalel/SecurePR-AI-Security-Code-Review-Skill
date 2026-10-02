import jwt from 'jsonwebtoken';
export function authenticate(token, trustedPublicKey) {
  return jwt.verify(token, trustedPublicKey, { algorithms: ['RS256'], issuer: 'https://issuer.example.invalid', audience: 'catalog-api' });
}
