export function record(req, logger) {
  logger.info({ event: 'login', password: req.body.password });
}
