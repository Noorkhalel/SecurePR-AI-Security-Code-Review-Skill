export function calculate(req) {
  const { left, right, operation } = req.body;
  if (!Number.isFinite(left) || !Number.isFinite(right)) throw new Error('number');
  const ops = new Map([['add', (a, b) => a + b], ['multiply', (a, b) => a * b]]);
  const calculate = ops.get(operation);
  if (!calculate) throw new Error('operation');
  return calculate(left, right);
}
