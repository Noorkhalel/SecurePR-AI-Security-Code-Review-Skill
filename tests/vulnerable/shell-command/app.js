import { exec } from 'node:child_process';
export function register(app) {
  app.post('/render-label', (req, res) => {
    exec('printf %s ' + req.body.label, (err, output) => {
      if (err) return res.status(500).end();
      res.type('text').send(output);
    });
  });
}
