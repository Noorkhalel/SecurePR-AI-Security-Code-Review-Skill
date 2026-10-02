import { createHmac } from 'node:crypto';
const signingSecret = 'SYNTHETIC_TEST_KEY_NOT_A_REAL_SECRET';
export function signSession(value) {
  return createHmac('sha256', signingSecret).update(value).digest('hex');
}
