type Profile = { displayName: string };
export async function profile(req: any, db: any) {
  if (typeof req.body.displayName !== 'string') throw new Error('name');
  const patch: Profile = { displayName: req.body.displayName };
  return db.user.update({ where: { id: req.actor.id }, data: patch });
}
