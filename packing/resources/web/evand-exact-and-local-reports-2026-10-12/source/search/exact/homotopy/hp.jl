# High-precision evaluation of the exported system with exact integer/rational coefficients:
# multivariate Horner trees (about one multiplication per term), Newton with a half-precision Jacobian.
using HomotopyContinuation, LinearAlgebra

abstract type HNode end
struct Leaf <: HNode
    c::Rational{BigInt}
end
struct Inner <: HNode
    var::Int
    ks::Vector{Int}             # exponents of `var`, descending
    ch::Vector{HNode}
end

function build(E::AbstractMatrix, C::AbstractVector, v::Int, n::Int)
    v > n && return Leaf(sum(C))
    ks = sort(unique(E[v, :]), rev = true)
    if ks == [0]
        return build(E, C, v + 1, n)
    end
    Inner(v, ks, [build(E[:, E[v, :] .== k], C[E[v, :] .== k], v + 1, n) for k in ks])
end

struct HPoly
    root::HNode
    n::Int
    maxd::Int
end
function hpoly(f, vars)
    E, C = exponents_coefficients(Expression(f), vars)
    Cq = [Rational{BigInt}(to_number(Expression(c))) for c in C]
    HPoly(build(E, Cq, 1, length(vars)), length(vars), maximum(E))
end
hpoly_grad(f, vars) = [hpoly(differentiate(f, v), vars) for v in vars]

const CB = Complex{BigFloat}
cval(c::Rational{BigInt}) = c.den == 1 ? CB(BigFloat(c.num)) : CB(BigFloat(c.num) / BigFloat(c.den))

ev(nd::Leaf, P) = cval(nd.c)
function ev(nd::Inner, P)
    p = P[nd.var]
    acc = ev(nd.ch[1], P)
    for j in 2:length(nd.ks)
        acc = acc * p[nd.ks[j-1] - nd.ks[j] + 1] + ev(nd.ch[j], P)
    end
    nd.ks[end] > 0 && (acc *= p[nd.ks[end] + 1])
    acc
end
val(f::HPoly, P) = ev(f.root, P)

function powers(x::Vector{CB}, maxd)
    [begin
        p = Vector{CB}(undef, maxd + 1); p[1] = one(x[i])
        for d in 1:maxd; p[d+1] = p[d] * x[i]; end; p
    end for i in eachindex(x)]
end

# H: polys, G: gradient polys (G[i][j] = dH_i/dx_j).  Newton levels doubling to `bits`; J at the previous level.
function newton_hp(H, G, x0, bits, maxd)
    n = length(x0)
    x = CB.(x0)
    levels = vcat([64 * 2^k for k in 0:30 if 64 * 2^k < bits], [bits])
    J = nothing
    step(b) = setprecision(BigFloat, b) do
        x = CB.(x); P = powers(x, maxd)
        x = x .- CB.(J) \ [val(h, P) for h in H]
    end
    for (li, b) in enumerate(levels)
        jb = li == 1 ? b : levels[li-1]
        setprecision(BigFloat, jb) do
            P = powers(CB.(x), maxd)
            J = [val(G[i][j], P) for i in 1:n, j in 1:n]
        end
        step(b)
    end
    step(bits)
    setprecision(BigFloat, bits) do
        P = powers(x, maxd)
        x, maximum(abs(val(h, P)) for h in H)
    end
end

# Newton from a point already accurate to ~bits_have bits, doubling to bits_target (J at the previous level).
function newton_up(H, G, x::Vector{CB}, bits_have, bits_target, maxd)
    n = length(x); b = bits_have
    while b < bits_target
        nb = min(2b, bits_target)
        J = setprecision(BigFloat, b) do
            P = powers(CB.(x), maxd)
            [val(G[i][j], P) for i in 1:n, j in 1:n]
        end
        x = setprecision(BigFloat, nb) do
            xx = CB.(x); P = powers(xx, maxd)
            xx .- CB.(J) \ [val(h, P) for h in H]
        end
        b = nb
    end
    setprecision(BigFloat, bits_target) do
        P = powers(x, maxd)
        x, maximum(abs(val(h, P)) for h in H)
    end
end
