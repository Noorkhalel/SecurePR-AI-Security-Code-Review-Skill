export function register(app) {
  app.get('/weather', async (req, res) => {
    const url = new URL('https://weather.example.invalid/current');
    url.searchParams.set('city', String(req.query.city));
    const response = await fetch(url, { redirect: 'error' });
    res.json(await response.json());
  });
}
