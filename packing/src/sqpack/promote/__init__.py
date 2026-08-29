"""The middle of the symbolic promotion pipeline.

The front end (source reconstruction) and the back end (`sqpack.field`,
`sqpack.verify`) were built first, so an exact atlas entry could be checked but never
derived.  This package holds the steps between them.

Each step reports what it measured and refuses when it cannot decide.  A step that
cannot fail has not been tested, and a step that succeeds by widening a tolerance is
worse than one that refuses.
"""
