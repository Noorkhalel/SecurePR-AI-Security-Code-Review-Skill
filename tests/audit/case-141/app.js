export async function suspend(req, res, db) {
  if (req.actor.role !== 'admin') return res.sendStatus(403);
  await db.account.update({ where: { id: req.params.id }, data: { suspended: true } });
  return res.sendStatus(204);
}
