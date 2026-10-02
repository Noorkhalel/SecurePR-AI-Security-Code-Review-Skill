import { cleanHTML } from './missing-library.js';
export function greeting(req, res) {
  res.type('html').send(cleanHTML(req.query.name));
}
