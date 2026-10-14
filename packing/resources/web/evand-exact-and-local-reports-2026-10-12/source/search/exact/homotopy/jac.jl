using HomotopyContinuation, LinearAlgebra
include(ARGS[1])
J = differentiate(F, tvars)
Jt = [Float64(evaluate(j, tvars => tstar)) for j in J]
println("singular values of dF at t*: ", svdvals(Jt))
