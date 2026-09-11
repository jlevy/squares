// The motion modes the buttons offer, in the order they are laid out.
() => Array.from(document.querySelectorAll('#phase-seg button')).map(b => b.dataset.phase)
