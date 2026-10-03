export async function remove(req, db) {
  return db.note.deleteMany({ where: { id: req.params.id, ownerId: req.actor.id } });
}
