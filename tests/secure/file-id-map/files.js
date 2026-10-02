const documents = new Map([['help', '/srv/public-docs/help.txt']]);
export async function loadDocument(id, readFile) {
  const file = documents.get(id);
  if (!file) throw new Error('Unknown document');
  return readFile(file, 'utf8');
}
