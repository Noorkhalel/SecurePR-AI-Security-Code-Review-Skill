export async function lookup(req, collection) {
  if (typeof req.body.category !== 'string') throw new Error('category');
  const selector = { category: req.body.category };
  return collection.find(selector).toArray();
}
