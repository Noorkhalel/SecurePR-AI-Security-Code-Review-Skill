export const GET = protectedRoute(async (actor, db, id) => db.invoice.findUnique({ where: { id } }));
