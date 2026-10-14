# Raise the precision of refine.jl output: ./jl.sh refine_up.jl SYSTEM IN_BITS IN OUT_BITS OUT
include("hp.jl")
include(ARGS[1])
bin, fin, bout, fout = parse(Int, ARGS[2]), ARGS[3], parse(Int, ARGS[4]), ARGS[5]
H = [hpoly(f, tvars) for f in F]; G = [hpoly_grad(f, tvars) for f in F]
HS = [hpoly(Sn, tvars), hpoly(Sd, tvars)]
k = length(tvars)
maxd = max(maximum(h.maxd for h in H), maximum(h.maxd for h in HS))
done = Set{Int}()
isfile(fout) && for l in eachline(fout); push!(done, parse(Int, split(l)[1])); end
open(fout, "a") do io
    for l in eachline(fin)
        f = split(l)
        j = parse(Int, f[1]); j in done && continue
        x = setprecision(BigFloat, bin) do
            [CB(parse(BigFloat, f[4+2i-1]), parse(BigFloat, f[4+2i])) for i in 1:k]
        end
        x, res = newton_up(H, G, x, bin, bout, maxd)
        setprecision(BigFloat, bout) do
            P = powers(x, maxd)
            S = val(HS[1], P) / val(HS[2], P)
            g(z) = string(real(z)) * " " * string(imag(z))
            println(io, j, " ", Float64(log10(res + big(2.0)^-(bout + 64))), " ", g(S), " ", join(g.(x), " "))
            flush(io)
        end
    end
end
