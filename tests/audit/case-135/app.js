export async function preview(req, fetch) {
  const url = new URL(req.body.url);
  if (url.origin !== 'https://catalog.example') throw new Error('origin');
  return (await fetch(url, { redirect: 'follow' })).text();
}
