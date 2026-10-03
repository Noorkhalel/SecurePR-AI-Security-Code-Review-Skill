export function logRequest(req, logger) {
  logger.info({ event: 'request', headers: req.headers });
}
