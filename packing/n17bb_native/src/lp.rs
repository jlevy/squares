//! Stateful S4 LP/OBBT port. The session retains exactly the tableau produced by
//! `solve_lp`; reloading between it and `tighten` would change warm-start arithmetic.
use crate::tinylp::{MAX_COLUMNS, MAX_ROWS, TinyLP};
use crate::{Box4, Iv, dual_bound_impl, max};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

type Outcome = (String, f64, Vec<f64>, Vec<f64>, bool);
type BoundEvent = (usize, f64, f64, Vec<f64>);
type TightenOutcome = (Option<Vec<Box4>>, Vec<BoundEvent>, Option<String>);

#[pyclass]
/// One warm-started LP and bound-tightening session.
pub(crate) struct LpSession {
    lp: TinyLP,
    columns: Vec<Vec<usize>>,
    exact: Vec<Vec<Iv>>,
    exact_rhs: Vec<Iv>,
    norms: Vec<f64>,
    boxes: Vec<Box4>,
    stepped: bool,
    tightened: bool,
}
fn spans(boxes: &[Box4]) -> Vec<Iv> {
    boxes
        .iter()
        .flat_map(|b| [(b.0, b.1), (b.2, b.3)])
        .collect()
}
#[pymethods]
impl LpSession {
    #[new]
    /// Load the pilot's sparse rows and current square boxes into a session.
    fn new(
        columns: Vec<Vec<usize>>,
        values: Vec<Vec<f64>>,
        rhs: Vec<f64>,
        norms: Vec<f64>,
        exact: Vec<Vec<Iv>>,
        exact_rhs: Vec<Iv>,
        boxes: Vec<Box4>,
    ) -> PyResult<Self> {
        let m = columns.len();
        let n = 2 * boxes.len() + 1;
        if boxes.is_empty()
            || n > MAX_COLUMNS
            || m > MAX_ROWS
            || [
                values.len(),
                rhs.len(),
                norms.len(),
                exact.len(),
                exact_rhs.len(),
            ]
            .iter()
            .any(|&l| l != m)
        {
            return Err(PyValueError::new_err(
                "expected 1..15 boxes, <=512 rows and matching row dimensions",
            ));
        }
        let mut a = vec![vec![0.0; n]; m];
        for i in 0..m {
            if columns[i].len() != values[i].len()
                || columns[i].len() != exact[i].len()
                || columns[i].iter().any(|&c| c >= n - 1)
            {
                return Err(PyValueError::new_err(
                    "invalid row columns or coefficient lengths",
                ));
            }
            for (&c, &v) in columns[i].iter().zip(&values[i]) {
                a[i][c] += v;
            }
            a[i][n - 1] += -1.0;
        }
        let ranges = spans(&boxes);
        let lo = ranges.iter().map(|s| s.0).chain([-1.0]).collect();
        let hi = ranges.iter().map(|s| s.1).chain([f64::INFINITY]).collect();
        let mut cost = vec![0.0; n];
        cost[n - 1] = 1.0;
        let mut lp = TinyLP::new();
        lp.load(a, rhs, lo, hi, cost)?;
        Ok(Self {
            lp,
            columns,
            exact,
            exact_rhs,
            norms,
            boxes,
            stepped: false,
            tightened: false,
        })
    }
    /// Solve the relaxation once and check its interval dual closure.
    fn lp_step(&mut self, lp_positive: f64) -> PyResult<Outcome> {
        if self.stepped {
            return Err(PyValueError::new_err(
                "lp_step must be called once per session",
            ));
        }
        self.stepped = true;
        let (status, value, point, mut duals) = self.lp.solve()?;
        for y in &mut duals {
            *y = max(0.0, *y);
        }
        let closed = status == "optimal"
            && !(value <= lp_positive)
            && dual_bound_impl(
                &self.columns,
                &self.exact,
                &self.exact_rhs,
                &self.norms,
                &duals,
                &spans(&self.boxes),
                None,
            )? > 0.0;
        Ok((
            status,
            value,
            point[..2 * self.boxes.len()].to_vec(),
            duals,
            closed,
        ))
    }
    /// Tighten every coordinate bound while retaining the relaxation's basis.
    fn tighten(&mut self) -> PyResult<Option<Vec<Box4>>> {
        Ok(self.tighten_impl(false)?.0)
    }
    /// Return accepted bounds in pilot order, followed by any empty-bounds reason.
    fn tighten_recorded(&mut self) -> PyResult<TightenOutcome> {
        self.tighten_impl(true)
    }
}
impl LpSession {
    fn tighten_impl(&mut self, record: bool) -> PyResult<TightenOutcome> {
        if !self.stepped || self.tightened {
            return Err(PyValueError::new_err(
                "tighten requires one preceding lp_step and may be called once",
            ));
        }
        self.tightened = true;
        let mut events = Vec::new();
        let k = self.boxes.len();
        let n = 2 * k + 1;
        let mut bounds: Vec<[f64; 4]> = self.boxes.iter().map(|b| [b.0, b.1, b.2, b.3]).collect();
        self.lp.set_col_bounds(n - 1, 0.0, 0.0)?;
        for column in 0..2 * k {
            let (square, axis) = (column / 2, column % 2);
            for sign in [1.0, -1.0] {
                let mut cost = vec![0.0; n];
                cost[column] = sign;
                self.lp.set_cost(cost)?;
                let (status, _, _, mut duals) = self.lp.solve()?;
                if status != "optimal" {
                    continue;
                }
                for y in &mut duals {
                    *y = max(0.0, *y);
                }
                let current: Vec<Iv> = bounds
                    .iter()
                    .flat_map(|b| [(b[0], b[1]), (b[2], b[3])])
                    .collect();
                let bound = dual_bound_impl(
                    &self.columns,
                    &self.exact,
                    &self.exact_rhs,
                    &self.norms,
                    &duals,
                    &current,
                    Some((column, sign)),
                )?;
                let slot = 2 * axis + usize::from(sign <= 0.0);
                let improved = (sign > 0.0 && bound > bounds[square][slot])
                    || (sign < 0.0 && -bound < bounds[square][slot]);
                if improved {
                    bounds[square][slot] = if sign > 0.0 { bound } else { -bound };
                    if record {
                        events.push((column, sign, bound, duals));
                    }
                }
                let (lo, hi) = (bounds[square][2 * axis], bounds[square][2 * axis + 1]);
                if lo > hi {
                    return Ok((None, events, Some("bounds".to_owned())));
                }
                self.lp.set_col_bounds(column, lo, hi)?;
            }
        }
        Ok((
            Some(bounds.iter().map(|b| (b[0], b[1], b[2], b[3])).collect()),
            events,
            None,
        ))
    }
}
#[pyfunction]
/// Run a standalone relaxation step without retaining its session.
fn lp_step(
    columns: Vec<Vec<usize>>,
    values: Vec<Vec<f64>>,
    rhs: Vec<f64>,
    norms: Vec<f64>,
    exact: Vec<Vec<Iv>>,
    exact_rhs: Vec<Iv>,
    boxes: Vec<Box4>,
    lp_positive: f64,
) -> PyResult<Outcome> {
    LpSession::new(columns, values, rhs, norms, exact, exact_rhs, boxes)?.lp_step(lp_positive)
}
#[pyfunction]
/// Recreate the pilot's solve followed by its warm-started tightening loop.
fn tighten(
    columns: Vec<Vec<usize>>,
    values: Vec<Vec<f64>>,
    rhs: Vec<f64>,
    norms: Vec<f64>,
    exact: Vec<Vec<Iv>>,
    exact_rhs: Vec<Iv>,
    boxes: Vec<Box4>,
    k: usize,
) -> PyResult<Option<Vec<Box4>>> {
    if k != boxes.len() {
        return Err(PyValueError::new_err("k differs from box count"));
    }
    let mut session = LpSession::new(columns, values, rhs, norms, exact, exact_rhs, boxes)?;
    // Recreate the preceding solve_lp tableau, including the failed-solve case.
    session.lp.solve()?;
    session.stepped = true;
    session.tighten()
}
pub(crate) fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<LpSession>()?;
    m.add_function(wrap_pyfunction!(lp_step, m)?)?;
    m.add_function(wrap_pyfunction!(tighten, m)?)?;
    Ok(())
}
