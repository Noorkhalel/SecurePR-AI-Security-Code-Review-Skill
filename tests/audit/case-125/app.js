import path from 'node:path';
export function read(req, fs) {
  const file = path.resolve('/srv/reports', req.params.name);
  if (!file.startsWith('/srv/reports')) throw new Error('outside');
  return fs.readFile(file);
}
