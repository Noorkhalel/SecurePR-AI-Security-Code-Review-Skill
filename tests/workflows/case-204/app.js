export function ship(state, actor, orderId) {
  if (!actor) return false;
  const order = state.orders.get(orderId);
  if (!order || order.ownerId !== actor.id || order.tenantId !== actor.tenantId) return false;
  if (order.state !== 'paid') return false;
  state.shipments.push({ orderId, address: order.address });
  order.state = 'shipped';
  return true;
}
