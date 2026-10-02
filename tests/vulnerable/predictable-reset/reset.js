export async function issueReset(userId, store) {
  const token = String(Math.floor(Math.random() * 1000000));
  await store.save({ userId, token, expiresAt: Date.now() + 600000 });
  return token;
}
