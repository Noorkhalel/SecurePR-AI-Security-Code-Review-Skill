import { execFile } from 'node:child_process';
export function label(value, callback) {
  if (typeof value !== 'string' || !/^[A-Za-z0-9 ]{1,40}$/.test(value)) throw new Error('Invalid label');
  execFile('/usr/bin/printf', ['%s', value], { shell: false }, callback);
}
