"""The locally injective half-angle chart on fixed-side square-packing configurations.

A configuration of `n` unit squares at a fixed container side is `n` centres and `n`
angles, so its natural home is `(R^2 x S^1)^n`, which is not an algebraic set. The chart
here replaces each angle by the tangent of its half increment from the pose:

    delta_k = 2 * atan(u_k),    cos delta_k = (1 - u_k^2) / (1 + u_k^2),
                                sin delta_k = 2 * u_k / (1 + u_k^2).

Three properties make that substitution the right instrument, and each is checked here by
exact computation rather than asserted:

- **it is injective**, so a chart point and a configuration are the same thing and a curve
  in one is a curve in the other -- `injectivity_certificate`;
- **its image is a neighborhood** of the pose in the configuration space, namely every
  configuration with no square turned by exactly half a turn, so nothing local is lost --
  same certificate;
- **it rationalises every constraint**: after multiplying by `1 + u^2`, every containment
  and every separating-axis inequality is a polynomial, and the multiplier is a positive
  quantity so the inequality's sign is unchanged -- `denominator_certificate`.

The denominators are not merely positive on some declared neighborhood. `1 + u^2 - 1` is
literally `u^2`, a square, so `1 + u^2 >= 1` on the whole real line, and the certificate
records that sum-of-squares witness with its margin. Clearing by a quantity whose sign was
only sampled would be the exact failure this instrument exists to avoid.

Chart variables are ordered `(a_k, b_k, u_k)` for `k = 0 .. n-1`: `a` and `b` displace the
centre and `u` is the half-angle parameter, so variable `3k + 2` is square `k`'s rotation.
That ordering matches `devtools.assess_n5_rigidity.variable_names`, which is what makes the
`T-012` binding a coordinate-by-coordinate comparison.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqpack.field import FieldElement, NumberField
from sqpack.local_rigidity.polynomial import Poly

DOF = 3
"""Chart coordinates per square: two of displacement and one half-angle."""

Point = tuple[FieldElement, FieldElement]
PolyPoint = tuple[Poly, Poly]


class ChartPreconditionError(ValueError):
    """The chart's declared algebra did not survive its own exact checks.

    Raised before any margin is computed. A chart whose denominator can vanish, or whose
    rotation matrix is not a positive multiple of an orthogonal one, produces polynomials
    that are not the constraints they claim to be -- and they would still evaluate and
    still have signs.
    """


@dataclass(frozen=True, slots=True)
class HalfAngleTransform:
    """The rationalising substitution, as data, so a wrong one can be tested.

    `denominator` and `matrix` are the cleared form of `R(2 atan(u))`: the true rotation is
    `matrix(u) / denominator(u)`. The identities that make that true --
    `matrix^T matrix = denominator^2 I` and `denominator >= 1` -- are checked, not assumed,
    which is what lets `controls.wrong_chart` hand in a plausible impostor and be refused.
    """

    name: str
    denominator_coefficients: tuple[int, int, int]
    """`denominator(u) = c0 + c1 u + c2 u^2`, low degree first."""

    matrix_builder: str
    """Either `half-angle` for the true matrix, or a named deviation used by controls."""

    def denominator(self, field: NumberField, arity: int, index: int) -> Poly:
        u = Poly.variable(field, arity, index)
        one = Poly.constant(field, arity, field.one)
        c0, c1, c2 = (field.rational(value) for value in self.denominator_coefficients)
        return one.scale(c0) + u.scale(c1) + (u * u).scale(c2)

    def matrix(self, field: NumberField, arity: int, index: int) -> tuple[Poly, ...]:
        """`(m00, m01, m10, m11)` of the cleared rotation matrix."""
        u = Poly.variable(field, arity, index)
        one = Poly.constant(field, arity, field.one)
        diagonal = one - u * u
        off = u.scale(field.rational(2))
        if self.matrix_builder == "half-angle":
            return (diagonal, -off, off, diagonal)
        if self.matrix_builder == "unscaled-off-diagonal":
            return (diagonal, -u, u, diagonal)
        if self.matrix_builder == "sign-flipped-off-diagonal":
            return (diagonal, off, off, diagonal)
        raise ChartPreconditionError(f"unknown matrix builder {self.matrix_builder!r}")


TANGENT_HALF_ANGLE = HalfAngleTransform(
    name="tangent-half-angle",
    denominator_coefficients=(1, 0, 1),
    matrix_builder="half-angle",
)
"""`u = tan(delta / 2)`: denominator `1 + u^2`, matrix `[[1-u^2, -2u], [2u, 1-u^2]]`."""


@dataclass(frozen=True, slots=True)
class BasePose:
    """One exact packing pose: the point the chart is centred on."""

    label: str
    field: NumberField
    side: FieldElement
    centres: tuple[Point, ...]
    corners: tuple[tuple[Point, ...], ...]

    @property
    def count(self) -> int:
        return len(self.centres)

    def offset(self, square: int, corner: int) -> Point:
        cx, cy = self.centres[square]
        px, py = self.corners[square][corner]
        return (px - cx, py - cy)

    def base_normal(self, square: int, edge: int) -> Point:
        """Outward unit normal of one base edge, exactly.

        Corners run counter-clockwise, so for `p -> q` the outward normal is `(dy, -dx)`;
        unit edges make it a unit vector with no scaling.
        """
        corners = self.corners[square]
        (px, py), (qx, qy) = corners[edge], corners[(edge + 1) % len(corners)]
        return (qy - py, px - qx)

    def edge_count(self, square: int) -> int:
        return len(self.corners[square])


def pose_from_case(label: str, build_result: tuple) -> BasePose:
    """Wrap a `cases.*.packing.build()` triple as a chart base pose."""
    squares, side, field = build_result
    quarter = field.rational(1) / field.rational(4)
    centres: list[Point] = []
    for square in squares:
        xs = [corner[0] for corner in square]
        ys = [corner[1] for corner in square]
        centres.append((sum(xs[1:], xs[0]) * quarter, sum(ys[1:], ys[0]) * quarter))
    return BasePose(
        label=label,
        field=field,
        side=side,
        centres=tuple(centres),
        corners=tuple(tuple(square) for square in squares),
    )


@dataclass(frozen=True, slots=True)
class SumOfSquaresWitness:
    """`polynomial - margin` written as a square, proving `polynomial >= margin`."""

    subject: str
    margin: str
    square_root: str
    verified: bool


@dataclass(frozen=True, slots=True)
class IdentityCheck:
    """One exact polynomial identity that had to hold before anything else ran."""

    name: str
    statement: str
    holds: bool


class Chart:
    """The half-angle chart at one base pose, with its cleared polynomial geometry."""

    def __init__(
        self, pose: BasePose, transform: HalfAngleTransform = TANGENT_HALF_ANGLE
    ) -> None:
        self.pose = pose
        self.transform = transform
        self.field = pose.field
        self.arity = pose.count * DOF
        self._denominators = tuple(
            transform.denominator(self.field, self.arity, square * DOF + 2)
            for square in range(pose.count)
        )
        self._matrices = tuple(
            transform.matrix(self.field, self.arity, square * DOF + 2)
            for square in range(pose.count)
        )

    # -- names -------------------------------------------------------------

    def variable_names(self) -> list[str]:
        return [
            name
            for square in range(self.pose.count)
            for name in (f"a{square}", f"b{square}", f"u{square}")
        ]

    def origin(self) -> list[FieldElement]:
        """The chart point that is the base pose."""
        return [self.field.zero] * self.arity

    # -- cleared geometry --------------------------------------------------

    def denominator(self, square: int) -> Poly:
        """`1 + u_k^2`: the positive quantity every constraint of square `k` clears by."""
        return self._denominators[square]

    def _constant(self, value: FieldElement) -> Poly:
        return Poly.constant(self.field, self.arity, value)

    def centre(self, square: int) -> PolyPoint:
        """The centre as a chart polynomial: base centre plus the two displacements."""
        cx, cy = self.pose.centres[square]
        a = Poly.variable(self.field, self.arity, square * DOF)
        b = Poly.variable(self.field, self.arity, square * DOF + 1)
        return (self._constant(cx) + a, self._constant(cy) + b)

    def cleared_corner(self, square: int, corner: int) -> PolyPoint:
        """`D_k * p_{k,j}`: the corner with its single denominator cleared."""
        denominator = self.denominator(square)
        cx, cy = self.centre(square)
        m00, m01, m10, m11 = self._matrices[square]
        rx, ry = (self._constant(value) for value in self.pose.offset(square, corner))
        return (
            denominator * cx + m00 * rx + m01 * ry,
            denominator * cy + m10 * rx + m11 * ry,
        )

    def cleared_normal(self, square: int, edge: int) -> PolyPoint:
        """`D_k * n_{k,e}`: the outward edge normal with its denominator cleared."""
        m00, m01, m10, m11 = self._matrices[square]
        nx, ny = (self._constant(value) for value in self.pose.base_normal(square, edge))
        return (m00 * nx + m01 * ny, m10 * nx + m11 * ny)

    # -- certificates ------------------------------------------------------

    def denominator_certificate(self) -> list[SumOfSquaresWitness]:
        """Exactly: every cleared denominator is at least one, hence strictly positive.

        The witness is a literal square, so the bound holds on all of `R^{3n}` and a
        fortiori on any declared neighborhood. Nothing here is a sampled radius.
        """
        witnesses: list[SumOfSquaresWitness] = []
        one = self._constant(self.field.one)
        for square in range(self.pose.count):
            u = Poly.variable(self.field, self.arity, square * DOF + 2)
            residual = self.denominator(square) - one
            witnesses.append(
                SumOfSquaresWitness(
                    subject=f"D{square} = {self.transform.name} denominator in u{square}",
                    margin="1",
                    square_root=f"u{square}",
                    verified=residual == u * u,
                )
            )
        return witnesses

    def orthogonality_certificate(self) -> list[IdentityCheck]:
        """Exactly: `M(u)^T M(u) = D(u)^2 I`, so `M / D` really is a rotation.

        Without this the "normal" the pair constraints use need not be a unit vector, and
        the constant `1/2` in a corner-versus-edge gap -- the half-width of a unit square
        along its own edge normal -- would be the wrong constant.
        """
        checks: list[IdentityCheck] = []
        for square in range(self.pose.count):
            m00, m01, m10, m11 = self._matrices[square]
            squared = self.denominator(square) * self.denominator(square)
            zero = Poly.zero(self.field, self.arity)
            checks.append(
                IdentityCheck(
                    name=f"orthogonality/square-{square}",
                    statement=(f"M(u{square})^T M(u{square}) = D{square}^2 * I over Q(sqrt 2)"),
                    holds=(
                        m00 * m00 + m10 * m10 == squared
                        and m01 * m01 + m11 * m11 == squared
                        and m00 * m01 + m10 * m11 == zero
                    ),
                )
            )
        return checks

    def base_normal_certificate(self) -> list[IdentityCheck]:
        """Exactly: every base edge normal is a unit vector."""
        checks: list[IdentityCheck] = []
        one = self.field.one
        for square in range(self.pose.count):
            for edge in range(self.pose.edge_count(square)):
                nx, ny = self.pose.base_normal(square, edge)
                checks.append(
                    IdentityCheck(
                        name=f"unit-normal/square-{square}/edge-{edge}",
                        statement="n . n = 1 exactly in Q(sqrt 2)",
                        holds=(nx * nx + ny * ny - one).is_zero(),
                    )
                )
        return checks

    def injectivity_certificate(self) -> list[IdentityCheck]:
        """Exactly: the half-angle substitution is injective with a punctured-circle image.

        Four polynomial identities in the auxiliary ring `Q[u, v]` or `Q[c, s]` do all the
        work, and each is checked by exact polynomial equality rather than by sampling.

        - *Injective, step one.* `cos delta(u) = cos delta(v)` cross-multiplies to
          `2(v^2 - u^2) = 0`, so `v = +-u`.
        - *Injective, step two.* With `v = -u`, `sin delta(u) = sin delta(v)`
          cross-multiplies to `4u(1 + u^2) = 0`, and `1 + u^2 >= 1`, so `u = v = 0`.
          Together: distinct chart angles are distinct rotations.
        - *Image, exclusion.* `(1 - u^2)/(1 + u^2) = -1` needs `2 = 0`, so the half turn
          is the one rotation outside the image -- and it is at distance `pi` from the
          pose, so the image still contains a full neighborhood of every square's angle.
        - *Image, inclusion.* For any `(c, s)` on the unit circle with `c != -1`, the
          value `u = s / (1 + c)` maps back to `(c, s)`; the two identities below are what
          make that substitution exact rather than checked at a few points.
        """
        field = self.field
        two = 2
        u = Poly.variable(field, two, 0)
        v = Poly.variable(field, two, 1)
        one = Poly.constant(field, two, field.one)
        left_cos = (one - u * u) * (one + v * v)
        right_cos = (one - v * v) * (one + u * u)
        cos_gap = left_cos - right_cos
        wanted_cos = (v * v - u * u).scale(field.rational(2))

        sin_with_v_negative = (u * (one + u * u)).scale(field.rational(4))

        c = Poly.variable(field, two, 0)
        s = Poly.variable(field, two, 1)
        one2 = Poly.constant(field, two, field.one)
        relation = s * s + c * c - one2
        # (1 + c)^2 + s^2 = 2(1 + c) modulo c^2 + s^2 = 1.
        inclusion_denominator = ((one2 + c) * (one2 + c) + s * s) - (one2 + c).scale(
            field.rational(2)
        )
        # (1 + c)^2 - s^2 = 2c(1 + c) modulo c^2 + s^2 = 1.
        inclusion_numerator = ((one2 + c) * (one2 + c) - s * s) - (c * (one2 + c)).scale(
            field.rational(2)
        )
        return [
            IdentityCheck(
                name="injectivity/equal-cosine-forces-equal-squares",
                statement="(1-u^2)(1+v^2) - (1-v^2)(1+u^2) = 2(v^2 - u^2) in Q[u, v]",
                holds=cos_gap == wanted_cos,
            ),
            IdentityCheck(
                name="injectivity/equal-sine-at-v-equals-minus-u",
                statement="2u(1+u^2) - 2(-u)(1+u^2) = 4u(1+u^2), zero only at u = 0",
                holds=(
                    (u * (one + u * u)).scale(field.rational(2))
                    - ((-u) * (one + u * u)).scale(field.rational(2))
                    == sin_with_v_negative
                ),
            ),
            IdentityCheck(
                name="image/half-turn-is-the-only-omitted-rotation",
                statement="(1 - u^2) + (1 + u^2) = 2 != 0, so cos delta = -1 is unreachable",
                holds=((one - u * u) + (one + u * u)) == one.scale(field.rational(2)),
            ),
            IdentityCheck(
                name="image/every-other-rotation-is-attained",
                statement=(
                    "with c^2 + s^2 = 1 and c != -1, u = s/(1+c) gives 1+u^2 = 2/(1+c) "
                    "and 1-u^2 = 2c/(1+c); both reduce to multiples of c^2 + s^2 - 1"
                ),
                holds=(inclusion_denominator == relation and inclusion_numerator == -relation),
            ),
        ]

    def require_valid(self) -> None:
        """Refuse a chart whose own algebra does not check out."""
        failures = [
            witness.subject
            for witness in self.denominator_certificate()
            if not witness.verified
        ]
        failures += [
            check.name
            for group in (
                self.orthogonality_certificate(),
                self.base_normal_certificate(),
                self.injectivity_certificate(),
            )
            for check in group
            if not check.holds
        ]
        if failures:
            raise ChartPreconditionError(
                f"the {self.transform.name!r} chart failed {len(failures)} of its own exact "
                f"preconditions (first: {failures[0]}); its cleared polynomials are not the "
                "constraints they claim to be"
            )
