export function register(app, requireSession, db) {
  app.patch('/profile', requireSession, async (req, res) => {
    await db.user.update({ where: { id: req.user.id }, data: req.body });
    res.status(204).end();
  });
}
