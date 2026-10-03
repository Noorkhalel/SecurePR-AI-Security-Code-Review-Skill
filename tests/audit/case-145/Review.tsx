import { loadReview } from './storage.js';
export async function Review({ id, db }) {
  const review = await loadReview(db, id);
  return <section dangerouslySetInnerHTML={{ __html: review.text }} />;
}
