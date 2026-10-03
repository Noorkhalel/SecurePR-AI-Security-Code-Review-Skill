export async function list(req, db) {
  const order = req.query.sort;
  return db.query('SELECT title FROM public_books ORDER BY ' + order);
}
