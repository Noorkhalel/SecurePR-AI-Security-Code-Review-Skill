export function register(app, db) {
  app.post('/lookup', async (req, res) => {
    const result = await db.collection('public_items').findOne({ slug: req.body.slug });
    res.json(result);
  });
}
