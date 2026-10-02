import { search } from './service.js';
export function register(app, db) {
  app.get('/search', async (req, res) => res.json(await search(db, req.query.term)));
}
