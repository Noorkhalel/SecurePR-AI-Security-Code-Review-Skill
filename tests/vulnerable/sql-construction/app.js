export function register(app, db) {
  app.get('/catalog', async (req, res) => {
    const term = req.query.term;
    const result = await db.query("SELECT title FROM catalog WHERE title = '" + term + "'");
    res.json(result.rows);
  });
}
