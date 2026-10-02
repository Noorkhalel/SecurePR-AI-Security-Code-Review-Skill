const routes = new Map([['home', '/home'], ['settings', '/settings']]);
export function redirectAfterLogin(req, res) {
  res.redirect(routes.get(req.query.next) ?? '/home');
}
