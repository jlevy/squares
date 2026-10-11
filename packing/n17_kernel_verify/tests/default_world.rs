//! Bind the compiled default world to the declared exact world independently of code provenance.

use n17_kernel_verifier::{pyjson, verify};

#[test]
fn embedded_world_matches_declared_exact_cover() {
    let declared = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("cells/cover.json");
    let bytes = std::fs::read(&declared).expect("declared exact cover is present");
    let external = verify::file_cells(
        declared.to_str().expect("fixture path is UTF-8"),
        &pyjson::digest(&bytes),
    )
    .expect("declared exact cover parses");
    let embedded = verify::cover_cells().expect("compiled default world is present");
    assert_eq!(embedded.cap, external.cap);
    assert_eq!(embedded.names, external.names);
    assert_eq!(embedded.polygons, external.polygons);
    assert_eq!(embedded.names.len(), 24);
}
