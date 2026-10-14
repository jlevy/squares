# Which solutions of F = 0 are genuine solutions of the contact system (A(t) z + b(t) = 0 consistent, rank A full)?
#   ./jl.sh filter.jl work/n29_system.jl work/n29_sols.txt work/n29_genuine.txt
using HomotopyContinuation, LinearAlgebra, Printf
include(ARGS[1])
solfile, out = ARGS[2], ARGS[3]
k = length(tvars)
nz = length(zvars)
zi = Dict(v => i for (i, v) in enumerate(zvars))
iS = zi["S"]
# compile every row coefficient (num, den) to a fast evaluator
ex = Expression[]
for (c, kk) in rows
    for (v, (nu, de)) in c
        push!(ex, Expression(nu)); push!(ex, Expression(de))
    end
    push!(ex, Expression(kk[1])); push!(ex, Expression(kk[2]))
end
push!(ex, Expression(Sn)); push!(ex, Expression(Sd))
fx = CompiledSystem(System(ex; variables = tvars))
buf = zeros(ComplexF64, length(ex))
function AbS(t)
    HomotopyContinuation.evaluate!(buf, fx, t)
    A = zeros(ComplexF64, length(rows), nz); b = zeros(ComplexF64, length(rows))
    j = 1; minden = Inf
    for (ri, (c, kk)) in enumerate(rows)
        for (v, _) in c
            A[ri, zi[v]] = buf[j] / buf[j+1]; minden = min(minden, abs(buf[j+1])); j += 2
        end
        b[ri] = buf[j] / buf[j+1]; minden = min(minden, abs(buf[j+1])); j += 2
    end
    A, b, buf[j] / buf[j+1], minden
end
lines = readlines(solfile)
nG = 0; nR = 0
open(out, "w") do io
    for l in lines
        f = split(l)
        f[2] == "F" || continue
        v = parse.(Float64, f[3:end])
        t = ComplexF64[complex(v[2i-1], v[2i]) for i in 1:k]
        A, b, Sf, minden = AbS(t)
        if !(all(isfinite, A) && all(isfinite, b))
            @printf(io, "x %s nonfinite S=NaN Sz=NaN t=%s\n", f[1], join(string.(t), " "))
            continue
        end
        sc = maximum(abs, A); sb = maximum(abs, b)
        sv = svdvals(A)
        z = A \ (-b)
        res = norm(A * z + b) / (sc * norm(z) + sb)
        cond_ = sv[1] / sv[end]
        ok = res < 1e-8 && cond_ < 1e10 && minden > 1e-10
        global nG += ok
        isreal_ = maximum(abs, imag.(t)) < 1e-9
        global nR += ok && isreal_
        @printf(io, "%s %s %s res=%.2e cond=%.2e minden=%.2e S=%s Sz=%s t=%s\n", ok ? "G" : "x", f[1], isreal_ ? "R" : "C",
                res, cond_, minden, string(Sf), string(z[iS]), join(string.(t), " "))
    end
end
println("finite solutions: ", count(l -> split(l)[2] == "F", lines), "; genuine: ", nG, " (real: ", nR, ")")
