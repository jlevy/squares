# High-precision consistency check of the contact system at candidate solutions (filter.jl's borderline rejects).
#   ./jl.sh hpfilter.jl SYSTEM FILTER_OUT MAXRES OUT
include("hp.jl")
include(ARGS[1])
maxres = parse(Float64, ARGS[3])
H = [hpoly(f, tvars) for f in F]; G = [hpoly_grad(f, tvars) for f in F]
maxd0 = maximum(h.maxd for h in H)
zi = Dict(v => i for (i, v) in enumerate(zvars)); nz = length(zvars)
R = [( [(zi[v], hpoly(nu, tvars), hpoly(de, tvars)) for (v, (nu, de)) in c], hpoly(kk[1], tvars), hpoly(kk[2], tvars)) for (c, kk) in rows]
HS = [hpoly(Sn, tvars), hpoly(Sd, tvars)]
maxd = max(maxd0, maximum(maximum(max(a[2].maxd, a[3].maxd) for a in r[1]; init = 0) for r in R), maximum(h.maxd for h in HS))
nG = 0
open(ARGS[4], "w") do io
for l in eachline(ARGS[2])
    f = split(l)
    (f[1] == "x" || (get(ENV, "GS", "") == "1" && f[1] == "G" && f[2] == "S")) || continue
    (get(ENV, "ALLX", "") == "1" || f[2] == "N") || continue
    nw = parse(Int, get(ENV, "NW", "1")); w = parse(Int, get(ENV, "W", "0"))
    global lineno = (@isdefined(lineno) ? lineno : 0) + 1
    (lineno - 1) % nw == w || continue
    m = match(r"res=(\S+)", l); m === nothing && continue
    r0 = parse(Float64, m.captures[1]); (isnan(r0) || r0 > maxres) && continue
    occursin("NaN", split(l, " t=")[2]) && continue
    t = [parse(ComplexF64, strip(s)) for s in split(split(l, " t=")[2], r"(?<=im) ")]
    x, res = try newton_hp(H, G, t, 3000, maxd0) catch e; (CB.(t), big(Inf)) end
    isfinite(res) || (println(stderr, "junk    newton failed"); continue)
    setprecision(BigFloat, 3000) do
        P = powers(x, maxd)
        A = zeros(CB, length(R), nz); b = zeros(CB, length(R))
        for (ri, (ents, kn, kd)) in enumerate(R)
            for (j, nu, de) in ents; A[ri, j] = val(nu, P) / val(de, P); end
            b[ri] = val(kn, P) / val(kd, P)
        end
        Q = qr(A)
        z = Q \ (-b)
        rr = norm(A * z + b) / (norm(A) * norm(z) + norm(b))
        S = val(HS[1], P) / val(HS[2], P)
        Sz = z[zi["S"]]
        svr = let Jb = [val(G[i][j], P) for i in 1:length(F), j in 1:length(tvars)]
            for j in axes(Jb, 2); c = maximum(abs.(Jb[:, j])); c > 0 && (Jb[:, j] ./= c); end   # column scaling at full precision
            for i in axes(Jb, 1); c = maximum(abs.(Jb[i, :])); c > 0 && (Jb[i, :] ./= c); end
            sv = svdvals(ComplexF64.(Jb)); sv[end] / sv[1] end
        g = Float64(log10(rr + big(10.0)^-2000)) < -500 && Float64(log10(res + big(10.0)^-2000)) < -800 &&
            isfinite(S) && isfinite(Sz) && abs(S - Sz) < big(10.0)^-500 * max(1, abs(S)) && svr > 1e-300
        global nG += g
        println(stderr, g ? "GENUINE " : "junk    ", "lowprec res=", r0, " hp log10 res=", round(Float64(log10(rr + big(10.0)^-2000))),
                " F res ", round(Float64(log10(res + big(10.0)^-2000))), " S=", ComplexF64(S), " Sz=", ComplexF64(Sz))
        g && println(io, "G N C S=", ComplexF64(S), " Sz=0 t=", join(string.(ComplexF64.(x)), " "))
    end
end
end
println(stderr, "genuine after high-precision check: $nG")
