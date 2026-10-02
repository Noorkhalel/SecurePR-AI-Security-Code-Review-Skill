export function lookup(req, db) {
  return db.query('SELECT title FROM catalog WHERE title = $1', [req.query.term]);
}
