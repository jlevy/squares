# Match per-coordinate candidates into roots: all combinations, scored by |F| and |S - target|; Newton-polish the best.
#   ./jl.sh combo.jl SYSTEM "targets" "c1" "c2" "c3" "c4" "c5" OUT
using HomotopyContinuation, LinearAlgebra
include(ARGS[1])
pc(s) = [complex(parse.(Float64, split(p, ","))...) for p in split(s, ";")]
targets = pc(ARGS[2]); C = [pc(ARGS[i]) for i in 3:7]; out = ARGS[8]
Fs = System(F; variables = tvars); Sf = System([Sn, Sd]; variables = tvars)
open(out, "w") do io
for (qi, q) in enumerate(targets)
    best = []
    for idx in Iterators.product((1:length(c) for c in C)...)
        x = ComplexF64[C[i][idx[i]] for i in 1:5]
        v = Sf(x); S = v[1] / v[2]
        push!(best, (norm(Fs(x)) / (1 + norm(x))^26, abs(S - q), x))
    end
    sort!(best, by = b -> b[1] + b[2])
    for b in best[1:3]; println("target $qi: |F| $(b[1]) |S-q| $(b[2])"); end
    r = newton(Fs, best[1][3]; max_iters = 30)
    y = solution(r); v = Sf(y); S = v[1] / v[2]; sv = svdvals(jacobian(Fs, y))
    println("  newton: success $(is_success(r)), |S - q| = $(abs(S - q)), sv ratio $(sv[end] / sv[1]), moved $(norm(y - best[1][3]))")
    println(io, "G N C S=", q, " Sz=0 t=", join(string.(best[1][3]), " "))
end
end
