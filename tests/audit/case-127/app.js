export function storePassword(password, salt, crypto) {
  return crypto.scryptSync(password, salt, 64, { N: 32768, r: 8, p: 1, maxmem: 67108864 }).toString('hex');
}
