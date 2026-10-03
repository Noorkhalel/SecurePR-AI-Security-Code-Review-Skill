export function calculate(req) {
  const expression = req.body.expression;
  return Function('return (' + expression + ')')();
}
