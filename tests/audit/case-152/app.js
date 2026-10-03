export async function redeem(actor, code, db) {
  return db.serializableTransaction(async tx => {
    const coupon = await tx.coupon.consumeUnused({ code, ownerId: actor.id });
    if (!coupon) throw new Error('unavailable');
    await tx.balance.increment(actor.id, coupon.value);
  });
}
