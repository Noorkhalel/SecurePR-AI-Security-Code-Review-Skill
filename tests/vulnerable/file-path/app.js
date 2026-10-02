import path from 'node:path';
import { readFile } from 'node:fs/promises';
export function register(app) {
  app.get('/download', async (req, res) => {
    const file = path.join('/srv/public-docs', req.query.name);
    res.type('text').send(await readFile(file, 'utf8'));
  });
}
