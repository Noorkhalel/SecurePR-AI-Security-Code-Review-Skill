export async function upload(req, blobs) {
  const id = await blobs.put(req.file.bytes);
  return id;
}
export async function download(req, res, blobs) {
  res.type(req.query.type).send(await blobs.get(req.params.id));
}
