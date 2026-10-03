export async function purchase(req, catalog, orders) {
  const item = await catalog.get(req.body.sku);
  return orders.charge({ userId: req.actor.id, cents: item.priceCents + req.body.shippingCents });
}
