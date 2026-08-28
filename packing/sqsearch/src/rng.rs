//! Counter-based seeding, so a chain's stream depends on `(seed, chain)` and not
//! on how rayon happened to schedule it.
//!
//! The determinism discipline is the one recorded in this project's `FrankenSim`
//! study: key the stream by identity, never by arrival order, so that basin
//! statistics are reproducible and a reported configuration can be regenerated
//! from the numbers in its artifact.

/// `SplitMix64`, used only to turn `(seed, chain)` into a well-mixed state.
#[inline]
fn splitmix64(x: &mut u64) -> u64 {
    *x = x.wrapping_add(0x9E37_79B9_7F4A_7C15);
    let mut z = *x;
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}

/// xoshiro256++: fast, well-tested, and small enough to hold per chain.
pub struct Rng {
    s: [u64; 4],
}

impl Rng {
    /// Derive a chain's stream from the campaign seed and the chain index alone.
    pub fn keyed(seed: u64, chain: u64) -> Self {
        let mut z = seed ^ chain.wrapping_mul(0x9E37_79B9_7F4A_7C15);
        Rng {
            s: [
                splitmix64(&mut z),
                splitmix64(&mut z),
                splitmix64(&mut z),
                splitmix64(&mut z),
            ],
        }
    }

    #[inline(always)]
    pub fn next_u64(&mut self) -> u64 {
        let result = self.s[0]
            .wrapping_add(self.s[3])
            .rotate_left(23)
            .wrapping_add(self.s[0]);
        let t = self.s[1] << 17;
        self.s[2] ^= self.s[0];
        self.s[3] ^= self.s[1];
        self.s[1] ^= self.s[2];
        self.s[0] ^= self.s[3];
        self.s[2] ^= t;
        self.s[3] = self.s[3].rotate_left(45);
        result
    }

    /// Uniform in [0, 1).
    #[inline(always)]
    pub fn f64(&mut self) -> f64 {
        ((self.next_u64() >> 11) as f64) * (1.0 / 9_007_199_254_740_992.0)
    }

    /// Uniform in [-1, 1).
    #[inline(always)]
    pub fn signed(&mut self) -> f64 {
        self.f64() * 2.0 - 1.0
    }

    #[inline(always)]
    pub fn below(&mut self, bound: usize) -> usize {
        (self.next_u64() % bound as u64) as usize
    }
}
