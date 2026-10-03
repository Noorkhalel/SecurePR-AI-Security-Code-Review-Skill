// Authored synthetic example. The supplied actor represents a verified session.
export function updateProfile(actor, profileId, body, store) {
  if (!actor) return { status: 401 };
  const profile = store.get(profileId);
  if (!profile || profile.ownerId !== actor.id || profile.tenantId !== actor.tenantId) {
    return { status: 404 };
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)
      || typeof body.displayName !== 'string' || body.displayName.trim().length === 0) {
    return { status: 422 };
  }
  store.replace(profileId, { ...profile, ...body });
  return { status: 204 };
}
