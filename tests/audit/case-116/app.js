export async function changeEmail(req, accounts) { return accounts.beginEmailChange(req.user.id, req.body.email); }
