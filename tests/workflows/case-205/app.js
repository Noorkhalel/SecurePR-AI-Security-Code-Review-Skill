export function redeem(state, actor, rewardId) {
  if (!actor) return false;
  const reward = state.rewards.get(rewardId);
  const account = state.accounts.get(actor.id);
  if (!reward || !account || reward.ownerId !== actor.id || reward.used) return false;
  account.credit += reward.amount;
  reward.used = true;
  return true;
}
