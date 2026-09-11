// Which of these ids are in the page? o.ids is the list to look for.
(o) => o.ids.filter((id) => document.getElementById(id) !== null)
