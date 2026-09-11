// What the page's own data says about one size. o.n is the size.
(o) => JSON.parse(document.getElementById('atlas-data').textContent).facts[String(o.n)]
