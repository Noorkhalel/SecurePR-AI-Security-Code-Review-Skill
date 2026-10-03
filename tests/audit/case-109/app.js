export function logRequest(req, logger) {
  logger.info({ event: 'request', method: req.method });
}
