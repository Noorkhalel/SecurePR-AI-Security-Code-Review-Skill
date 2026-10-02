"use server";
import { session } from '../session';
import { db } from '../db';
export async function removeDocument(id: string) {
  const actor = await session();
  if (!actor) throw new Error('Unauthenticated');
  await db.document.delete({ where: { id } });
}
