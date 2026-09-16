// Run every `squaresMath.batch` call the queue-watchdog control holds.
() => /** @type {SquaresQueueControl} */ (__squaresQueueControl).release();
