# Application contract

requireSession authenticates all ordinary and admin users, with no role check. Only admins may delete accounts. users.deleteById unconditionally deletes the supplied ID. No gateway or outer policy enforces roles.
