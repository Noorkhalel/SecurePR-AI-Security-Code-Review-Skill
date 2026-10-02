export function search(req, db) {
  return db.query("SELECT title FROM catalog WHERE title = '" + req.query.term + "'");
}
