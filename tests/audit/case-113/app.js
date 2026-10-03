import { requireAdmin } from './policy.js';
export async function resetQuota(req, db) {
  const target = await db.user.findUnique({ where: { id: req.params.id } });
  requireAdmin(req.actor);
  return db.quota.reset(target.id);
}
