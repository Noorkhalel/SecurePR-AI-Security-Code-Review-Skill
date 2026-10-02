export async function disableUser(actor, id, db) {
  if (actor.role !== 'admin') throw new Error('Forbidden');
  return db.user.updateMany({ where: { id, tenantId: actor.tenantId }, data: { enabled: false } });
}
