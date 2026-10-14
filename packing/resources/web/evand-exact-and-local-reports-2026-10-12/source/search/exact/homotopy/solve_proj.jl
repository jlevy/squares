# Multi-projective solve: each class parameter t_i = a_i / b_i on P^1, so large |t_i| are ordinary points.
#   JULIA_NUM_THREADS=3 ./jl.sh solve_proj.jl work/n29_system.jl OUT [seed]
using HomotopyContinuation, LinearAlgebra
include(ARGS[1])
out = ARGS[2]
seed = length(ARGS) >= 3 ? parse(UInt32, ARGS[3]) : 0x29292929
k = length(tvars)
@var a[1:k] b[1:k]
function homog(f)
    E, C = exponents_coefficients(f, tvars)
    d = [maximum(E[i, :]) for i in 1:k]
    sum(C[j] * prod(a[i]^E[i, j] * b[i]^(d[i] - E[i, j]) for i in 1:k) for j in 1:size(E, 2))
end
Fh = [homog(f) for f in F]
sys_ = System(Fh; variable_groups = [[a[i], b[i]] for i in 1:k])
careful = length(ARGS) >= 4 && ARGS[4] == "careful"
opts = careful ? (tracker_options = TrackerOptions(parameters = :conservative, extended_precision = true, max_steps = 50_000),
                  endgame_options = EndgameOptions(max_endgame_steps = 20_000, max_endgame_extended_steps = 20_000)) : NamedTuple()
@time res = solve(sys_; threading = true, show_progress = true, seed = seed, opts...)
println(res)
open(out, "w") do io
    for r in path_results(res)
        x = solution(r)
        ok = is_success(r)
        t = [x[2i-1] / x[2i] for i in 1:k]          # variable order a1,b1,a2,b2,... per group
        minb = minimum(abs(x[2i]) / norm(x[2i-1:2i]) for i in 1:k)
        println(io, ok ? (is_singular(r) ? "S" : "N") : "X", " ", is_singular(r) ? "s" : "r",
                " minb=", minb, " cond=", r.condition_jacobian, " ",
                join(("$(real(z)) $(imag(z))" for z in t), " "))
    end
end
println("variables: ", variables(sys_))
