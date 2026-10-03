export async function redeem(actor, code, db) {
  const coupon = await db.coupon.findUnique({ where: { code, ownerId: actor.id } });
  if (!coupon || coupon.used) throw new Error('unavailable');
  await db.balance.increment(actor.id, coupon.value);
  await db.coupon.markUsed(code);
}
