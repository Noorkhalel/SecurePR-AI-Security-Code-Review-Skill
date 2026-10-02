const notes = [];
export function register(app) {
  app.post('/notes', (req, res) => {
    notes.push(req.body.text);
    res.status(201).end();
  });
  app.get('/notes', (req, res) => {
    res.type('html').send(notes.map(text => `<p>${text}</p>`).join(''));
  });
}
