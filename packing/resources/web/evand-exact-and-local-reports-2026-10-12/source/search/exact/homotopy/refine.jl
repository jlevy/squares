# Refine the genuine non-singular solutions to BITS bits; one of each complex-conjugate pair (the system is real).
# Writes per solution: index, log10 residual, S (re im), t1..tk (re im), at full precision.
#   ./jl.sh refine.jl work/n29_system.jl work/n29_genuine.txt BITS WORKER NWORKERS OUT
include("hp.jl")
include(ARGS[1])
gfile, bits, w, nw, out = ARGS[2], parse(Int, ARGS[3]), parse(Int, ARGS[4]), parse(Int, ARGS[5]), ARGS[6]
H = [hpoly(f, tvars) for f in F]; G = [hpoly_grad(f, tvars) for f in F]
HS = [hpoly(Sn, tvars), hpoly(Sd, tvars)]
k = length(tvars)
maxd = max(maximum(h.maxd for h in H), maximum(h.maxd for h in HS))
sols = Vector{ComplexF64}[]
for l in eachline(gfile)
    startswith(l, "G N") || continue
    push!(sols, [parse(ComplexF64, strip(s)) for s in split(split(l, " t=")[2], r"(?<=im) ")])
end
function rep(t)        # true for real solutions and for one member of each conjugate pair
    j = findfirst(z -> abs(imag(z)) > 1e-9, t)
    j === nothing || imag(t[j]) > 0
end
reps = [j for j in eachindex(sols) if rep(sols[j])]
w == 0 && println(stderr, "$(length(sols)) solutions, $(length(reps)) to refine ",
                  "($(count(t -> all(z -> abs(imag(z)) <= 1e-9, t), sols)) real)")
mine = reps[w+1:nw:end]
done = Set{Int}()
isfile(out) && for l in eachline(out); push!(done, parse(Int, split(l)[1])); end
t0 = time(); c = 0
open(out, "a") do io
    for j in mine
        j in done && continue
        x, res = newton_hp(H, G, sols[j], bits, maxd)
        setprecision(BigFloat, bits) do
            P = powers(x, maxd)
            S = val(HS[1], P) / val(HS[2], P)
            f(z) = string(real(z)) * " " * string(imag(z))
            println(io, j, " ", Float64(log10(res + big(2.0)^-(bits + 64))), " ", f(S), " ", join(f.(x), " "))
            flush(io)
        end
        global c += 1
        c % 50 == 0 && println(stderr, "worker $w: $c / $(length(mine)), $(round((time() - t0) / c, digits=2)) s each")
    end
end
println(stderr, "worker $w done")
