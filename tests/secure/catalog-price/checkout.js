export async function checkout(actor, body, catalog, payments) {
  const item = await catalog.get(body.itemId);
  if (!item) throw new Error('Unknown item');
  return payments.chargeAndFulfill({ userId: actor.id, itemId: item.id, totalCents: item.priceCents });
}
