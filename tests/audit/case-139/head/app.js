export function record(req, logger) {
  logger.info({ event: 'login', result: 'attempt' });
}
