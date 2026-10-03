router.use(requireAdmin);
router.post('/archive', archive);
function archive(req) { return jobs.archiveAll(); }
