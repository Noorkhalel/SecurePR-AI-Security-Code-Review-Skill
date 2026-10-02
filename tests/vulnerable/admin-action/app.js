export function register(app, requireSession, users) {
  app.delete('/admin/users/:id', requireSession, async (req, res) => {
    await users.deleteById(req.params.id);
    res.status(204).end();
  });
}
