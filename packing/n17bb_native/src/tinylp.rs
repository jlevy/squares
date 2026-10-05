// Ported from the measured prototype. Its NumPy boundary was replaced by Rust
// vectors; the simplex arithmetic and pivot choices remain unchanged.
//! Dense dictionary simplex. Each row is `x_B = rhs - D x_N`.
//! Slack columns allow RHS changes without storing a full basis inverse.
use pyo3::exceptions::{PyIndexError, PyValueError};
use pyo3::prelude::*;
const FEAS: f64 = 1e-9;
const OPT: f64 = 1e-10;
const PIV: f64 = 1e-11;
const CAP: usize = 10000;
/// Largest number of LP columns (two centre coordinates per square, plus the depth).
pub(crate) const MAX_COLUMNS: usize = 31;
/// Largest number of LP rows.
pub(crate) const MAX_ROWS: usize = 512;

#[derive(Clone)]
struct Tableau {
    m: usize,
    n: usize,
    w: usize,
    d: Vec<f64>,
    basic: Vec<usize>,
    nonbasic: Vec<usize>,
}
impl Tableau {
    pub(crate) fn new(a: &[Vec<f64>], b: &[f64], n: usize) -> Self {
        let m = b.len();
        let w = (n + 5) & !3; // Pad each row to a multiple of four doubles.
        let mut t = Self {
            m,
            n,
            w,
            d: vec![0.; (m + 2) * w],
            basic: (n..n + m).collect(),
            nonbasic: (0..n).chain(std::iter::once(usize::MAX)).collect(),
        };
        for i in 0..m {
            t.d[i * w..i * w + n].copy_from_slice(&a[i]);
            t.d[i * w + n] = -1.;
            t.d[i * w + n + 1] = b[i];
        }
        t.d[(m + 1) * w + n] = 1.;
        t
    }
    fn pivot(&mut self, r: usize, s: usize) {
        let w = self.w;
        let p = self.d[r * w + s];
        let inv = 1. / p;
        let mut normalized = [0.; 2 * MAX_COLUMNS + 6]; // At most 2*n split variables plus artificial/RHS.
        let pivot_row = &mut normalized[..w];
        for (v, &old) in pivot_row.iter_mut().zip(&self.d[r * w..(r + 1) * w]) {
            *v = old * inv;
        }
        for (i, row) in self.d.chunks_exact_mut(w).enumerate() {
            if i == r {
                continue;
            }
            let v = row[s];
            if v != 0. {
                for (entry, &pr) in row.iter_mut().zip(pivot_row.iter()) {
                    *entry -= v * pr;
                }
            }
            row[s] = -v * inv;
        }
        self.d[r * w..(r + 1) * w].copy_from_slice(pivot_row);
        self.d[r * w + s] = inv;
        std::mem::swap(&mut self.basic[r], &mut self.nonbasic[s]);
    }
    fn primal(&mut self, phase: bool) -> &'static str {
        let obj = if phase { self.m + 1 } else { self.m };
        let w = self.w;
        for it in 0..CAP {
            let mut s = None;
            for j in 0..=self.n {
                if !phase && self.nonbasic[j] == usize::MAX {
                    continue;
                }
                if self.d[obj * w + j] < -OPT
                    && s.is_none_or(|k: usize| {
                        if it > 64 {
                            self.nonbasic[j] < self.nonbasic[k]
                        } else {
                            self.d[obj * w + j] < self.d[obj * w + k]
                        }
                    })
                {
                    s = Some(j);
                }
            }
            let Some(s) = s else {
                return "optimal";
            };
            let mut r = None;
            let mut best = f64::INFINITY;
            let mut label = usize::MAX;
            for (i, row) in self.d[..self.m * w].chunks_exact(w).enumerate() {
                if row[s] > PIV {
                    let ratio = row[self.n + 1].max(0.) / row[s];
                    if ratio < best - 1e-12
                        || ((ratio - best).abs() <= 1e-12 && self.basic[i] < label)
                    {
                        r = Some(i);
                        best = ratio;
                        label = self.basic[i];
                    }
                }
            }
            let Some(r) = r else {
                return "unbounded";
            };
            self.pivot(r, s);
        }
        "error"
    }
    fn phase_one(&mut self) -> &'static str {
        let w = self.w;
        let r = (0..self.m)
            .min_by(|&i, &j| self.d[i * w + self.n + 1].total_cmp(&self.d[j * w + self.n + 1]));
        if let Some(r) = r
            && self.d[r * w + self.n + 1] < -FEAS
        {
            self.pivot(r, self.n);
            let status = self.primal(true);
            if status != "optimal" {
                return "error";
            }
            if self.d[(self.m + 1) * w + self.n + 1] < -FEAS {
                return "infeasible";
            }
            if let Some(r) = self.basic.iter().position(|&v| v == usize::MAX)
                && let Some(s) = (0..=self.n)
                    .filter(|&j| self.nonbasic[j] != usize::MAX && self.d[r * w + j].abs() > PIV)
                    .max_by(|&j, &k| self.d[r * w + j].abs().total_cmp(&self.d[r * w + k].abs()))
            {
                self.pivot(r, s);
            }
            // An identically zero redundant row may retain the artificial variable.
        }
        "optimal"
    }
    fn cost(&mut self, c: &[f64]) {
        let w = self.w;
        let o = self.m * w;
        for j in 0..w {
            self.d[o + j] = 0.;
        }
        for j in 0..=self.n {
            if self.nonbasic[j] < self.n {
                self.d[o + j] = c[self.nonbasic[j]];
            }
        }
        for i in 0..self.m {
            if self.basic[i] < self.n {
                let cb = c[self.basic[i]];
                if cb == 0. {
                    continue;
                }
                for j in 0..w {
                    self.d[o + j] -= cb * self.d[i * w + j];
                }
            }
        }
    }
    fn rhs_change(&mut self, row: usize, delta: f64) {
        let slack = self.n + row;
        let rhs = self.n + 1;
        if let Some(i) = self.basic.iter().position(|&v| v == slack) {
            self.d[i * self.w + rhs] += delta;
        } else if let Some(j) = self.nonbasic.iter().position(|&v| v == slack) {
            for i in 0..self.m {
                self.d[i * self.w + rhs] += self.d[i * self.w + j] * delta;
            }
        }
    }
    fn shift_variable(&mut self, variable: usize, delta: f64) {
        if delta == 0. {
            return;
        }
        let rhs = self.n + 1;
        if let Some(i) = self.basic.iter().position(|&v| v == variable) {
            self.d[i * self.w + rhs] -= delta;
        } else if let Some(j) = self.nonbasic.iter().position(|&v| v == variable) {
            for row in self.d[..self.m * self.w].chunks_exact_mut(self.w) {
                row[rhs] -= row[j] * delta;
            }
        }
    }
    fn dual(&mut self) -> &'static str {
        let w = self.w;
        for _ in 0..CAP {
            let r = (0..self.m)
                .filter(|&i| self.d[i * w + self.n + 1] < -FEAS)
                .min_by_key(|&i| self.basic[i]);
            let Some(r) = r else {
                return "optimal";
            };
            let mut s = None;
            for j in 0..=self.n {
                if self.nonbasic[j] != usize::MAX && self.d[r * w + j] < -PIV {
                    let ratio = self.d[self.m * w + j].max(0.) / -self.d[r * w + j];
                    if s.is_none_or(|k: usize| {
                        let old = self.d[self.m * w + k].max(0.) / -self.d[r * w + k];
                        ratio < old - 1e-12
                            || ((ratio - old).abs() <= 1e-12 && self.nonbasic[j] < self.nonbasic[k])
                    }) {
                        s = Some(j);
                    }
                }
            }
            let Some(s) = s else {
                return "infeasible";
            };
            self.pivot(r, s);
        }
        "error"
    }
}

#[pyclass(name = "_TinyLP")]
#[derive(Default)]
/// Dense warm-started simplex exposed only as a differential-test seam.
pub(crate) struct TinyLP {
    a: Vec<Vec<f64>>,
    b: Vec<f64>,
    lo: Vec<f64>,
    hi: Vec<f64>,
    c: Vec<f64>,
    shift: Vec<f64>,
    map: Vec<(usize, f64)>,
    bound_rows: Vec<Option<usize>>,
    tab: Option<Tableau>,
    loaded: bool,
    cost_dirty: bool,
}
impl TinyLP {
    fn rebuild(&mut self) -> &'static str {
        let n = self.c.len();
        self.shift = vec![0.; n];
        self.map.clear();
        for j in 0..n {
            if self.lo[j].is_finite() {
                self.shift[j] = self.lo[j];
                self.map.push((j, 1.));
            } else if self.hi[j].is_finite() {
                self.shift[j] = self.hi[j];
                self.map.push((j, -1.));
            } else {
                self.map.push((j, 1.));
                self.map.push((j, -1.));
            }
        }
        let k = self.map.len();
        let mut a = Vec::new();
        let mut b = Vec::new();
        for (row, &rhs) in self.a.iter().zip(&self.b) {
            a.push(self.map.iter().map(|&(j, s)| row[j] * s).collect());
            b.push(rhs - row.iter().zip(&self.shift).map(|(v, s)| v * s).sum::<f64>());
        }
        self.bound_rows.clear();
        for j in 0..n {
            let mut row = None;
            // A lower or upper bound is implicit in z >= 0. Only a second
            // finite bound needs an explicit row.
            if self.lo[j].is_finite() && self.hi[j].is_finite() {
                row = Some(b.len());
                a.push(
                    self.map
                        .iter()
                        .map(|&(col, s)| if col == j { s } else { 0. })
                        .collect(),
                );
                b.push(self.hi[j] - self.shift[j]);
            }
            self.bound_rows.push(row);
        }
        let mut t = Tableau::new(&a, &b, k);
        let status = t.phase_one();
        if status != "optimal" {
            self.tab = None;
            return status;
        }
        t.cost(
            &self
                .map
                .iter()
                .map(|&(j, s)| self.c[j] * s)
                .collect::<Vec<_>>(),
        );
        self.cost_dirty = false;
        let status = t.primal(false);
        self.tab = Some(t);
        status
    }
    fn result(&self) -> (f64, Vec<f64>, Vec<f64>) {
        let Some(t) = self.tab.as_ref() else {
            return (f64::NAN, vec![0.0; self.c.len()], vec![0.0; self.b.len()]);
        };
        let mut x = self.shift.clone();
        for i in 0..t.m {
            if t.basic[i] < t.n {
                let (j, s) = self.map[t.basic[i]];
                x[j] += s * t.d[i * t.w + t.n + 1];
            }
        }
        let mut y = vec![0.; self.b.len()];
        for j in 0..=t.n {
            let id = t.nonbasic[j];
            if id >= t.n && id < t.n + y.len() {
                y[id - t.n] = t.d[t.m * t.w + j].max(0.);
            }
        }
        (x.iter().zip(&self.c).map(|(x, c)| x * c).sum(), x, y)
    }
    fn valid(&self, x: &[f64], y: &[f64]) -> bool {
        if x.iter().chain(y).any(|v| !v.is_finite()) {
            return false;
        }
        for (j, _) in x.iter().enumerate() {
            if x[j] < self.lo[j] - FEAS || x[j] > self.hi[j] + FEAS {
                return false;
            }
        }
        let mut gradient = self.c.clone();
        for (i, _) in y.iter().enumerate() {
            if y[i] != 0. {
                for (g, &a) in gradient.iter_mut().zip(&self.a[i]) {
                    *g += a * y[i];
                }
            }
            let ax = self.a[i].iter().zip(x).map(|(a, x)| a * x).sum::<f64>();
            let slack = self.b[i] - ax;
            if slack < -FEAS * (1. + self.b[i].abs())
                || (y[i] * slack).abs() > 1e-8 * (1. + y[i].abs())
            {
                return false;
            }
        }
        for (j, _) in x.iter().enumerate() {
            let g = gradient[j];
            if g > FEAS
                && (!self.lo[j].is_finite()
                    || (g * (x[j] - self.lo[j])).abs() > 1e-8 * (1. + g.abs()))
            {
                return false;
            }
            if g < -FEAS
                && (!self.hi[j].is_finite()
                    || (g * (self.hi[j] - x[j])).abs() > 1e-8 * (1. + g.abs()))
            {
                return false;
            }
        }
        true
    }
}

#[pymethods]
impl TinyLP {
    #[new]
    /// Create an unloaded simplex instance.
    pub(crate) fn new() -> Self {
        Self::default()
    }
    /// Replace the problem with dense rows, column bounds, and a minimization cost.
    pub(crate) fn load(
        &mut self,
        a: Vec<Vec<f64>>,
        b: Vec<f64>,
        lower: Vec<f64>,
        upper: Vec<f64>,
        cost: Vec<f64>,
    ) -> PyResult<()> {
        let (m, n) = (a.len(), cost.len());
        let lo = lower;
        let hi = upper;
        let c = cost;
        if a.iter().any(|row| row.len() != n)
            || m > MAX_ROWS
            || n == 0
            || n > MAX_COLUMNS
            || b.len() != m
            || lo.len() != n
            || hi.len() != n
            || c.len() != n
        {
            return Err(PyValueError::new_err(
                "expected m <= 512, 1 <= n <= 31 and matching dimensions",
            ));
        }
        if a.iter()
            .flatten()
            .chain(&b)
            .chain(&c)
            .any(|v| !v.is_finite())
            || lo.iter().any(|v| v.is_nan() || *v == f64::INFINITY)
            || hi.iter().any(|v| v.is_nan() || *v == f64::NEG_INFINITY)
        {
            return Err(PyValueError::new_err(
                "nonfinite data or invalid bound infinity",
            ));
        }
        *self = Self {
            a,
            b,
            lo,
            hi,
            c,
            loaded: true,
            ..Self::default()
        };
        Ok(())
    }
    /// Change the minimization cost while retaining primal feasibility.
    pub(crate) fn set_cost(&mut self, cost: Vec<f64>) -> PyResult<()> {
        let c = cost;
        if !self.loaded || c.len() != self.c.len() || c.iter().any(|v| !v.is_finite()) {
            return Err(PyValueError::new_err(
                "load first; cost must have n finite entries",
            ));
        }
        self.c = c;
        self.cost_dirty = true;
        Ok(())
    }
    /// Change one column's lower and upper bounds.
    pub(crate) fn set_col_bounds(&mut self, j: usize, lo: f64, hi: f64) -> PyResult<()> {
        if !self.loaded || j >= self.c.len() {
            return Err(PyIndexError::new_err("column out of range"));
        }
        if lo.is_nan() || hi.is_nan() || lo == f64::INFINITY || hi == f64::NEG_INFINITY {
            return Err(PyValueError::new_err("invalid bounds"));
        }
        if let Some(t) = self.tab.as_mut() {
            // Changing finite/infinite structure requires a fresh representation.
            let incompatible = lo.is_finite() != self.lo[j].is_finite()
                || hi.is_finite() != self.hi[j].is_finite();
            if incompatible {
                self.tab = None;
            } else {
                let Some(variable) = self.map.iter().position(|&(col, _)| col == j) else {
                    self.tab = None;
                    self.lo[j] = lo;
                    self.hi[j] = hi;
                    return Ok(());
                };
                if lo.is_finite() {
                    t.shift_variable(variable, lo - self.lo[j]);
                    self.shift[j] = lo;
                    if let Some(r) = self.bound_rows[j] {
                        t.rhs_change(r, hi - self.hi[j]);
                    }
                } else if hi.is_finite() {
                    t.shift_variable(variable, self.hi[j] - hi);
                    self.shift[j] = hi;
                }
            }
        }
        self.lo[j] = lo;
        self.hi[j] = hi;
        Ok(())
    }
    /// Solve or reoptimize and return status, value, primal point, and row duals.
    pub(crate) fn solve(&mut self) -> PyResult<(String, f64, Vec<f64>, Vec<f64>)> {
        if !self.loaded {
            return Err(PyValueError::new_err("load a problem before solve"));
        }
        let mut status = "infeasible";
        if !self.lo.iter().zip(&self.hi).any(|(l, u)| l > u) {
            if let Some(t) = self.tab.as_mut() {
                // Repair primal feasibility under the old (still dual feasible) objective first.
                status = t.dual();
                if status == "optimal" {
                    if self.cost_dirty {
                        t.cost(
                            &self
                                .map
                                .iter()
                                .map(|&(j, s)| self.c[j] * s)
                                .collect::<Vec<_>>(),
                        );
                        self.cost_dirty = false;
                    }
                    status = t.primal(false);
                }
                if status != "optimal" {
                    status = self.rebuild();
                }
            } else {
                status = self.rebuild();
            }
            if status == "optimal" {
                let (v, x, y) = self.result();
                if v.is_finite() && self.valid(&x, &y) {
                    return Ok((status.into(), v, x, y));
                }
                status = self.rebuild();
                if status == "optimal" {
                    let (v, x, y) = self.result();
                    if v.is_finite() && self.valid(&x, &y) {
                        return Ok((status.into(), v, x, y));
                    }
                    status = "error";
                }
            }
        }
        self.tab = None;
        Ok((
            status.into(),
            match status {
                "infeasible" => f64::INFINITY,
                "unbounded" => f64::NEG_INFINITY,
                _ => f64::NAN,
            },
            vec![0.; self.c.len()],
            vec![0.; self.b.len()],
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::TinyLP;

    fn solve(
        a: Vec<Vec<f64>>,
        b: Vec<f64>,
        lo: Vec<f64>,
        hi: Vec<f64>,
        cost: Vec<f64>,
    ) -> (String, f64, Vec<f64>, Vec<f64>) {
        let mut lp = TinyLP::new();
        lp.load(a, b, lo, hi, cost).expect("valid test LP");
        lp.solve().expect("test LP solves")
    }

    #[test]
    fn solves_a_bounded_minimization_problem() {
        let (status, value, point, duals) = solve(
            vec![vec![-1.0, -1.0]],
            vec![-3.0],
            vec![0.0, 0.0],
            vec![2.0, 4.0],
            vec![1.0, 2.0],
        );
        assert_eq!(status, "optimal");
        assert_eq!(value, 4.0);
        assert_eq!(point, vec![2.0, 1.0]);
        assert_eq!(duals, vec![2.0]);
    }

    #[test]
    fn reports_infeasible_bounds() {
        let (status, value, point, duals) =
            solve(Vec::new(), Vec::new(), vec![2.0], vec![1.0], vec![1.0]);
        assert_eq!(status, "infeasible");
        assert_eq!(value, f64::INFINITY);
        assert_eq!(point, vec![0.0]);
        assert_eq!(duals, Vec::<f64>::new());
    }

    #[test]
    fn retains_a_basis_across_bound_and_cost_changes() {
        let mut lp = TinyLP::new();
        lp.load(
            vec![vec![-1.0, -1.0]],
            vec![-2.0],
            vec![0.0, 0.0],
            vec![4.0, 4.0],
            vec![1.0, 0.0],
        )
        .expect("valid test LP");
        let first = lp.solve().expect("initial solve");
        assert_eq!(first.0, "optimal");
        assert_eq!(first.1, 0.0);

        lp.set_col_bounds(1, 0.0, 1.0).expect("valid bound");
        lp.set_cost(vec![1.0, 1.0]).expect("valid cost");
        let second = lp.solve().expect("warm solve");
        assert_eq!(second.0, "optimal");
        assert_eq!(second.1, 2.0);
    }
}
