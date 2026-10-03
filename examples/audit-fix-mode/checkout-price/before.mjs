// Authored synthetic example. A server-created cart contains the committed quote.
export function checkout(actor, cartId, body, store) {
  if (!actor) return { status: 401 };
  const cart = store.get(cartId);
  if (!cart || cart.ownerId !== actor.id || cart.tenantId !== actor.tenantId) {
    return { status: 404 };
  }
  if (cart.state !== 'open') return { status: 409 };
  const totalCents = body.totalCents ?? cart.totalCents;
  if (!Number.isSafeInteger(totalCents) || totalCents <= 0) return { status: 422 };
  store.complete(cartId, { cartId, totalCents, currency: cart.currency });
  return { status: 201 };
}
