export function saveReview(db, req) { return db.review.create({ data: { productId: req.body.productId, text: req.body.text } }); }
export function loadReview(db, id) { return db.review.findUnique({ where: { id } }); }
