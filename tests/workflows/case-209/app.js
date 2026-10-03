export function verifyEmail(state, actor, tokenId, requestedEmail, now) {
  if (!actor) return false;
  const token = state.tokens.get(tokenId);
  const user = state.users.get(actor.id);
  if (!user || !token || token.used || token.userId !== actor.id || token.expires <= now) return false;
  user.email = requestedEmail;
  user.emailVerified = true;
  token.used = true;
  return true;
}
