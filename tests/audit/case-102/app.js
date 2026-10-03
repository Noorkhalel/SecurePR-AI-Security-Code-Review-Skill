export async function upload(req, blobs) {
  const id = await blobs.put(req.file.bytes);
  return id;
}
export async function download(req, res, blobs) {
  res.set('Content-Disposition', 'attachment; filename="upload.bin"');
  res.set('X-Content-Type-Options', 'nosniff');
  res.type('application/octet-stream').send(await blobs.get(req.params.id));
}
