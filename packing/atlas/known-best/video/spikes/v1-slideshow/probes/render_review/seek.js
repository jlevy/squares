// Move the slideshow's clock to an instant and report what shows there. Takes {seconds}.
/** @param {{seconds: number}} o */
(o) => window.atlasVideo.seek(o.seconds);
