export async function remove(req, db) {
  const note = await db.note.findUnique({ where: { id: req.params.id } });
  if (note.ownerId !== req.actor.id) throw new Error('forbidden');
  return db.note.delete({ where: { id: note.id } });
}
