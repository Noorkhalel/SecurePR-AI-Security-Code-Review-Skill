// Authored synthetic example. Only displayName is editable through this operation.
export function updateProfile(actor, profileId, body, store) {
  if (!actor) return { status: 401 };
  const profile = store.get(profileId);
  if (!profile || profile.ownerId !== actor.id || profile.tenantId !== actor.tenantId) {
    return { status: 404 };
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)
      || typeof body.displayName !== 'string' || body.displayName.trim().length === 0
      || Object.keys(body).some(key => key !== 'displayName')) {
    return { status: 422 };
  }
  store.replace(profileId, { ...profile, displayName: body.displayName });
  return { status: 204 };
}
