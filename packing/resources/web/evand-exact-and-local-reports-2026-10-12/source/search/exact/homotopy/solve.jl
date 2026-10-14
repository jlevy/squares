# Polyhedral homotopy for the exported system: all isolated complex solutions of F = 0.
#   JULIA_NUM_THREADS=3 ./jl.sh solve.jl work/n29_system.jl work/n29_sols.txt
using HomotopyContinuation, LinearAlgebra
include(ARGS[1])
out = ARGS[2]
sys_ = System(F; variables = tvars)
@time res = solve(sys_; threading = true, show_progress = true, seed = length(ARGS) >= 3 ? parse(UInt32, ARGS[3]) : 0x29292929)
println(res)
ts = ComplexF64.(tstar)
open(out, "w") do io
    for r in results(res)
        r.solution === nothing && continue
        x = solution(r)
        println(io, is_singular(r) ? "S" : "N", " ", is_finite(r) ? "F" : "I", " ",
                join(("$(real(z)) $(imag(z))" for z in x), " "))
    end
end
d = minimum(norm(solution(r) - ts) for r in results(res) if is_finite(r))
println("closest solution to t*: distance ", d)
