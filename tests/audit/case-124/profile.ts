type Profile = { displayName: string };
export async function profile(req: any, db: any) {
  const patch = req.body as Profile;
  return db.user.update({ where: { id: req.actor.id }, data: patch });
}
