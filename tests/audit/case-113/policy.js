export function requireAdmin(actor) { if (actor.role !== 'admin') throw new Error('forbidden'); }
