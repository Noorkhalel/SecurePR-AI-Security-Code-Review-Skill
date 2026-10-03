import Profile from './Profile.tsx';
export default async function Page({ session, db }) {
  const user = await db.user.findUnique({ where: { id: session.actor.id } });
  return <Profile user={{ displayName: user.displayName }} />;
}
