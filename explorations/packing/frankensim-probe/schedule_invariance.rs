//! EXPERIMENT (added for external research; not part of FrankenSim).
//!
//! Does fs-rand's counter-based stream really make a stochastic search
//! schedule-independent? Draws the same logical work in three different
//! orders and compares the results bit for bit.

use fs_rand::{Stream, StreamKey};

const SEED: u64 = 0x5152_5354_5556_5758;
const KERNEL: u32 = 7;
const TILES: u32 = 64;
const DRAWS: u64 = 32;

fn tile_draws(tile: u32) -> Vec<u64> {
    let key = StreamKey {
        seed: SEED,
        kernel: KERNEL,
        tile,
    };
    let mut s = key.stream();
    (0..DRAWS).map(|_| s.next_u64()).collect()
}

fn main() {
    let sequential: Vec<(u32, Vec<u64>)> = (0..TILES).map(|t| (t, tile_draws(t))).collect();
    let mut reversed: Vec<(u32, Vec<u64>)> = (0..TILES).rev().map(|t| (t, tile_draws(t))).collect();
    let mut interleaved: Vec<(u32, Vec<u64>)> = Vec::new();
    for w in 0..5u32 {
        let mut t = w;
        while t < TILES {
            interleaved.push((t, tile_draws(t)));
            t += 5;
        }
    }

    reversed.sort_by_key(|(tile, _)| *tile);
    interleaved.sort_by_key(|(tile, _)| *tile);
    let all_equal = sequential == reversed && reversed == interleaved;
    assert!(all_equal, "schedule changed at least one generated word");
    println!("fs-rand schedule invariance ({TILES} tiles x {DRAWS} draws)");
    println!("  all generated words equal: {all_equal}");

    let key = StreamKey {
        seed: SEED,
        kernel: KERNEL,
        tile: 3,
    };
    let mut s = key.stream();
    let seq: Vec<u64> = (0..8).map(|_| s.next_u64()).collect();
    let direct: Vec<u64> = (0..4u64)
        .map(|i| {
            let w = Stream::at(key, i);
            u64::from(w[0]) | (u64::from(w[1]) << 32)
        })
        .collect();
    println!(
        "  random access matches sequential prefix: {}",
        seq.iter().take(4).eq(direct.iter())
    );

    let t0 = std::time::Instant::now();
    for i in 0..100_000u64 {
        std::hint::black_box(Stream::at(key, i));
    }
    let near = t0.elapsed();
    let t1 = std::time::Instant::now();
    for i in 0..100_000u64 {
        std::hint::black_box(Stream::at(key, u64::MAX / 2 + i));
    }
    let far = t1.elapsed();
    println!("  100k seeks near index 0: {near:?}");
    println!("  100k seeks near 2^63:    {far:?}   (O(1) random access)");
}
