include("hp.jl")
include(ARGS[1])
H = [hpoly(f, tvars) for f in F]
println("coeff types ok: ", typeof(H[1].C[1]), " max den ", maximum(maximum(c.den for c in h.C) for h in H))
maxd = maximum(maximum(h.E) for h in H)
function newton(x0; bits)
    x = Complex{BigFloat}.(x0)
    for b in vcat([64 * 2^k for k in 0:20 if 64 * 2^k < bits], [bits, bits])
        setprecision(BigFloat, b) do
            x = Complex{BigFloat}.(x)
            P = powers(x, maxd)
            vg = [valgrad(h, P, 5) for h in H]
            u = [a[1] for a in vg]; J = permutedims(hcat([a[2] for a in vg]...))
            x = x .- J \ u
        end
    end
    x
end
setprecision(BigFloat, 66500)
for bits in (2000, 66500)
    t0 = time()
    x = newton(ComplexF64.(tstar); bits = bits)
    println(bits, " bits: ", round(time() - t0, digits = 2), " s; |x - t*(70 digits)| = ",
            Float64(log10(norm(x .- big.(tstar)))))
end
