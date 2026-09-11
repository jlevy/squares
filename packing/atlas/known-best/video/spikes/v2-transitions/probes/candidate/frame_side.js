// The container side the record states for one frame. Takes {n}.
(o) => JSON.parse(document.getElementById('atlas-data').textContent).frames[String(o.n)].side
