using HomotopyContinuation
include(ARGS[1])
println("residuals at t*: ", [Float64(abs(evaluate(f, tvars => tstar))) for f in F])
@time println("mixed volume: ", mixed_volume(System(F)))
