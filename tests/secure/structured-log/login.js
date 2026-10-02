export async function login(body, auth, logger) {
  const result = await auth.verify(body.email, body.password);
  logger.info({ event: 'login', success: Boolean(result) });
  return result;
}
