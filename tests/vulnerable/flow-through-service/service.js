import { runQuery } from './storage.js';
export function search(db, text) {
  const normalized = text.trim();
  return runQuery(db, normalized);
}
