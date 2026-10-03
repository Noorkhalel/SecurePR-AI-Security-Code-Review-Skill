export function storePassword(password, salt, crypto) {
  return crypto.createHash('sha256').update(salt + password).digest('hex');
}
