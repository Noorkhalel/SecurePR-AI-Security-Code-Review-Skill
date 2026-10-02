import { protectedRoute } from './missing-policy.js';
export const handler = protectedRoute(async (req, res, db) => {
  res.json(await db.invoice.findUnique({ where: { id: req.params.id } }));
});
