import { randomUUID } from 'node:crypto';
export async function storeUpload(file, privateStore) {
  if (!Buffer.isBuffer(file.bytes) || file.bytes.length > 65536) throw new Error('Size');
  if (file.type !== 'text/plain') throw new Error('Type');
  const text = new TextDecoder('utf-8', { fatal: true }).decode(file.bytes);
  if (!/^[a-zA-Z0-9 .,!\r\n]*$/.test(text)) throw new Error('Content');
  const id = randomUUID();
  await privateStore.put(id, text, { contentType: 'text/plain', disposition: 'attachment' });
  return id;
}
