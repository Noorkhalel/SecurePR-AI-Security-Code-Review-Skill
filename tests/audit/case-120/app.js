export function render(req, childProcess) {
  return childProcess.execFile('/usr/bin/asset-render', ['--', req.body.label], { shell: false });
}
