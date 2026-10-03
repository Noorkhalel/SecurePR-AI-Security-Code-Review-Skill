export async function lookup(req, collection) {
  const selector = { category: req.body.category };
  return collection.find(selector).toArray();
}
