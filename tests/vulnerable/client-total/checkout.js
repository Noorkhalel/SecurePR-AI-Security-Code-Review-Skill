export async function checkout(user, body, catalog, payments) {
  const item = await catalog.get(body.itemId);
  if (!item) throw new Error('Unknown item');
  return payments.chargeAndFulfill({ userId: user.id, itemId: item.id, totalCents: body.totalCents });
}
