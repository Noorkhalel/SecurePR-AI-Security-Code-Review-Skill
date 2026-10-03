export function read(req, fs) {
  const files = new Map([['summary', '/srv/reports/summary.txt'], ['annual', '/srv/reports/annual.txt']]);
  const file = files.get(req.params.name);
  if (!file) throw new Error('unknown report');
  return fs.readFile(file);
}
