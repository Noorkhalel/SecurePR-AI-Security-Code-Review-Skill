export async function runQuery(db, value) {
  return db.query("SELECT title FROM catalog WHERE title = '" + value + "'");
}
