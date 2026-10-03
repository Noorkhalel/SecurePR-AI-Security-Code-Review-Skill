import { allowedInvites } from './policy.js';
export function invite(state, actor, email, role) {
  if (!actor || !allowedInvites[actor.role]) return false;
  state.invitations.push({ tenantId: actor.tenantId, email, role });
  return true;
}
