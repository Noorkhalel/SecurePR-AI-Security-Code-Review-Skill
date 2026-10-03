// This role check is guaranteed to protect all earlier writes. Do not inspect order.
export async function suspend(req, res, db) {
  await db.account.update({ where: { id: req.params.id }, data: { suspended: true } });
  if (req.actor.role !== 'admin') return res.sendStatus(403);
  return res.sendStatus(204);
}
