export async function payment(event, store) {
  if (await store.seen(event.id)) return;
  await store.settle(event);
  await store.remember(event.id);
}
