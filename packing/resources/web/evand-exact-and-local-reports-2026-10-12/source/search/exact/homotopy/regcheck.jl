# Keep candidates that are regular roots of F: Newton at 3000 bits converges (|F| < 1e-800) and dF is nonsingular.
#   ./jl.sh regcheck.jl SYSTEM CANDS OUT
include("hp.jl")
include(ARGS[1])
H = [hpoly(f, tvars) for f in F]; G = [hpoly_grad(f, tvars) for f in F]
maxd = maximum(h.maxd for h in H)
nk = 0; nr = 0
open(ARGS[3], "w") do io
    for l in eachline(ARGS[2])
        startswith(l, "G") || continue
        global nk += 1
        t = [parse(ComplexF64, strip(s)) for s in split(split(l, " t=")[2], r"(?<=im) ")]
        x, res = try newton_hp(H, G, t, 3000, maxd) catch e; (CB.(t), big(Inf)) end
        sv = setprecision(BigFloat, 3000) do
            P = powers(CB.(x), maxd)
            Jb = [val(G[i][j], P) for i in 1:length(F), j in 1:length(tvars)]
            for j in axes(Jb, 2); c = maximum(abs.(Jb[:, j])); c > 0 && (Jb[:, j] ./= c); end   # scale at full precision
            for i in axes(Jb, 1); c = maximum(abs.(Jb[i, :])); c > 0 && (Jb[i, :] ./= c); end
            svdvals(ComplexF64.(Jb))
        end
        moved = Float64(maximum(abs.(ComplexF64.(x) .- t)))
        ok = Float64(log10(res + big(10.0)^-2000)) < -800 && sv[end] / sv[1] > 1e-300 && moved < 1e-6
        S = split(split(l, " S=")[2], " Sz=")[1]
        println(stderr, ok ? "REGULAR " : "reject  ", rpad(S, 46), " log10res ", round(Float64(log10(res + big(10.0)^-2000))),
                " sv ratio ", sv[end] / sv[1], " moved ", moved)
        ok && (global nr += 1; println(io, l))
    end
end
println(stderr, "$nk candidates, $nr regular")
