export async function redeem(code, store, credit) {
  if (await store.used(code)) throw new Error('Used');
  await credit(code);
  await store.markUsed(code);
}
