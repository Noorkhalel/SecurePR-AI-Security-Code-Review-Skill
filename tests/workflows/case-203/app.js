export function recover(state, tokenId, requestedUserId, digest, now) {
  const token = state.tokens.get(tokenId);
  if (!token || token.used || token.expires <= now) return false;
  const user = state.users.get(requestedUserId);
  if (!user || token.userId !== requestedUserId) return false;
  token.used = true;
  user.passwordDigest = digest;
  return true;
}
