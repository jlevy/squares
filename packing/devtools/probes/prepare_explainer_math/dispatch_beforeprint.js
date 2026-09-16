// Dispatch `beforeprint`, as the browser does before printing.
() => dispatchEvent(new Event("beforeprint"));
