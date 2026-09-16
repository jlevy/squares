// The document's scroll width, read at once. `layout/document-size` reads it two frames later;
// this is for a caller that has already waited on the condition it measures after.
() => document.documentElement.scrollWidth;
