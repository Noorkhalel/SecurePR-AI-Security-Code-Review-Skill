import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';
export function register(app, multipart) {
  app.post('/upload', multipart.single('file'), async (req, res) => {
    const stored = randomUUID() + '.html';
    await writeFile('/srv/public/uploads/' + stored, req.file.buffer);
    res.json({ url: '/uploads/' + stored });
  });
}
