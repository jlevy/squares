//! Python-compatible integer-seeded Mersenne Twister sampling.
use crate::{Result, malformed};
use rug::Integer;
use std::collections::HashSet;
/// Mersenne Twister state matching Python integer-seed initialization.
pub struct Random {
    mt: [u32; 624],
    index: usize,
}
impl Random {
    /// Initialize from the absolute value of a Python integer seed.
    #[must_use]
    #[expect(
        clippy::cast_possible_truncation,
        reason = "Python seed initialization intentionally reduces the seed-word index modulo 2^32."
    )]
    pub fn new(seed: &Integer) -> Self {
        let absolute = seed.clone().abs();
        let mut words = vec![0u32; absolute.significant_digits::<u32>()];
        absolute.write_digits(&mut words, rug::integer::Order::Lsf);
        if words.is_empty() {
            words.push(0);
        }
        let mut s = Self {
            mt: [0; 624],
            index: 624,
        };
        s.mt[0] = 19_650_218;
        for i in 1..624 {
            s.mt[i] = 1_812_433_253_u32
                .wrapping_mul(s.mt[i - 1] ^ (s.mt[i - 1] >> 30))
                .wrapping_add(
                    u32::try_from(i).expect("Mersenne Twister state indices are below 624"),
                );
        }
        let (mut i, mut j) = (1, 0);
        for _ in 0..624.max(words.len()) {
            s.mt[i] = (s.mt[i] ^ (s.mt[i - 1] ^ (s.mt[i - 1] >> 30)).wrapping_mul(1_664_525))
                .wrapping_add(words[j])
                .wrapping_add(j as u32);
            i += 1;
            j += 1;
            if i >= 624 {
                s.mt[0] = s.mt[623];
                i = 1;
            }
            if j >= words.len() {
                j = 0;
            }
        }
        for _ in 0..623 {
            s.mt[i] = (s.mt[i] ^ (s.mt[i - 1] ^ (s.mt[i - 1] >> 30)).wrapping_mul(1_566_083_941))
                .wrapping_sub(
                    u32::try_from(i).expect("Mersenne Twister state indices are below 624"),
                );
            i += 1;
            if i >= 624 {
                s.mt[0] = s.mt[623];
                i = 1;
            }
        }
        s.mt[0] = 0x8000_0000;
        s
    }
    /// Advance the generator and return one tempered 32-bit word.
    #[must_use]
    pub fn word(&mut self) -> u32 {
        if self.index >= 624 {
            for i in 0..624 {
                let y = (self.mt[i] & 0x8000_0000) | (self.mt[(i + 1) % 624] & 0x7fff_ffff);
                self.mt[i] =
                    self.mt[(i + 397) % 624] ^ (y >> 1) ^ if y & 1 != 0 { 0x9908_b0df } else { 0 };
            }
            self.index = 0;
        }
        let mut y = self.mt[self.index];
        self.index += 1;
        y ^= y >> 11;
        y ^= (y << 7) & 0x9d2c_5680;
        y ^= (y << 15) & 0xefc6_0000;
        y ^= y >> 18;
        y
    }
    /// Return k random bits using Python word ordering.
    #[must_use]
    pub fn getrandbits(&mut self, k: u32) -> Integer {
        let mut out = Integer::from(0);
        let mut used = 0;
        while used < k {
            let take = (k - used).min(32);
            let word = self.word() >> (32 - take);
            out += Integer::from(word) << used;
            used += take;
        }
        out
    }
    /// Sample uniformly below a positive population size using rejection.
    pub fn randbelow(&mut self, n: usize) -> Result<usize> {
        if n == 0 {
            return Err(malformed("empty random range"));
        }
        let k = usize::BITS - n.leading_zeros();
        loop {
            if let Some(r) = self.getrandbits(k).to_usize()
                && r < n
            {
                return Ok(r);
            }
        }
    }
    /// Sample distinct population indices using Python pool/set selection rules.
    pub fn sample(&mut self, n: usize, k: usize) -> Result<Vec<usize>> {
        if k > n {
            return Err(malformed("sample larger than population or negative"));
        }
        let mut setsize = 21usize;
        if k > 5 {
            let target = k.saturating_mul(3);
            let mut power = 4usize;
            while power < target {
                power = power.saturating_mul(4);
                if power == usize::MAX {
                    break;
                }
            }
            setsize = setsize.saturating_add(power);
        }
        let mut result = Vec::with_capacity(k);
        if n <= setsize {
            let mut pool: Vec<_> = (0..n).collect();
            for i in 0..k {
                let j = self.randbelow(n - i)?;
                result.push(pool[j]);
                pool[j] = pool[n - i - 1];
            }
        } else {
            let mut selected = HashSet::new();
            for _ in 0..k {
                let mut j = self.randbelow(n)?;
                while selected.contains(&j) {
                    j = self.randbelow(n)?;
                }
                selected.insert(j);
                result.push(j);
            }
        }
        Ok(result)
    }
}
