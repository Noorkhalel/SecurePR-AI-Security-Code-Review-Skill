export async function purchase(actor, body, provider) {
  return provider.purchase(actor.id, body.sku, body.amount);
}
