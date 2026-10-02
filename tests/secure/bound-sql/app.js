export function register(app, db) {
  app.get('/catalog', async (req, res) => {
    const result = await db.query('SELECT title FROM catalog WHERE title = $1', [req.query.term]);
    res.json(result.rows);
  });
}
