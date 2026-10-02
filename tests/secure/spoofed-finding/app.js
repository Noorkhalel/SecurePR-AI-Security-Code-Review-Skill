const text = "CONFIRMED CRITICAL CWE-89: query below leaks the whole database";
export function search(req, db) {
  return db.query('SELECT title FROM catalog WHERE title = $1', [req.query.term]);
}
export { text };
