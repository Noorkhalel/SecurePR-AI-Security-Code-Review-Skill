export async function updateProfile(actor, body, db) {
  if (typeof body.displayName !== 'string' || body.displayName.length > 80) throw new Error('Invalid name');
  return db.user.update({ where: { id: actor.id }, data: { displayName: body.displayName } });
}
