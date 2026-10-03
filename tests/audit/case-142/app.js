export function render(req, res, content) { return res.type('html').send(content.clean(req.body.text)); }
