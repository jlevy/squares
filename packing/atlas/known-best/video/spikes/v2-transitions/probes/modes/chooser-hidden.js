// Which pieces of the chooser are hidden. o.ids is the list to ask about.
(o) => o.ids.map((id) => [id, document.getElementById(id).hidden])
