import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0320
open Sq19.Endgame.Reduction

theorem case0320 : checkNat 320 = true := by native_decide
#print axioms case0320

theorem case1344 : checkNat 1344 = true := by
  apply check_of_normalize (Case.ofNat 1344)
  have he : (Case.ofNat 1344).normalize = Case.ofNat 320 := by decide
  rw [he]
  exact case0320
#print axioms case1344

theorem case2368 : checkNat 2368 = true := by
  apply check_of_normalize (Case.ofNat 2368)
  have he : (Case.ofNat 2368).normalize = Case.ofNat 320 := by decide
  rw [he]
  exact case0320
#print axioms case2368

theorem case3392 : checkNat 3392 = true := by
  apply check_of_normalize (Case.ofNat 3392)
  have he : (Case.ofNat 3392).normalize = Case.ofNat 320 := by decide
  rw [he]
  exact case0320
#print axioms case3392

theorem case0321 : checkNat 321 = true := by native_decide
#print axioms case0321

theorem case2369 : checkNat 2369 = true := by
  apply check_of_normalize (Case.ofNat 2369)
  have he : (Case.ofNat 2369).normalize = Case.ofNat 321 := by decide
  rw [he]
  exact case0321
#print axioms case2369

theorem case0322 : checkNat 322 = true := by native_decide
#print axioms case0322

theorem case1346 : checkNat 1346 = true := by
  apply check_of_normalize (Case.ofNat 1346)
  have he : (Case.ofNat 1346).normalize = Case.ofNat 322 := by decide
  rw [he]
  exact case0322
#print axioms case1346

theorem case0323 : checkNat 323 = true := by native_decide
#print axioms case0323

theorem case0324 : checkNat 324 = true := by native_decide
#print axioms case0324

theorem case1348 : checkNat 1348 = true := by
  apply check_of_normalize (Case.ofNat 1348)
  have he : (Case.ofNat 1348).normalize = Case.ofNat 324 := by decide
  rw [he]
  exact case0324
#print axioms case1348

theorem case2372 : checkNat 2372 = true := by
  apply check_of_normalize (Case.ofNat 2372)
  have he : (Case.ofNat 2372).normalize = Case.ofNat 324 := by decide
  rw [he]
  exact case0324
#print axioms case2372

theorem case3396 : checkNat 3396 = true := by
  apply check_of_normalize (Case.ofNat 3396)
  have he : (Case.ofNat 3396).normalize = Case.ofNat 324 := by decide
  rw [he]
  exact case0324
#print axioms case3396

theorem case0325 : checkNat 325 = true := by native_decide
#print axioms case0325

theorem case2373 : checkNat 2373 = true := by
  apply check_of_normalize (Case.ofNat 2373)
  have he : (Case.ofNat 2373).normalize = Case.ofNat 325 := by decide
  rw [he]
  exact case0325
#print axioms case2373

theorem case0326 : checkNat 326 = true := by native_decide
#print axioms case0326

theorem case1350 : checkNat 1350 = true := by
  apply check_of_normalize (Case.ofNat 1350)
  have he : (Case.ofNat 1350).normalize = Case.ofNat 326 := by decide
  rw [he]
  exact case0326
#print axioms case1350

theorem case0327 : checkNat 327 = true := by native_decide
#print axioms case0327

theorem case0328 : checkNat 328 = true := by native_decide
#print axioms case0328

theorem case1352 : checkNat 1352 = true := by
  apply check_of_normalize (Case.ofNat 1352)
  have he : (Case.ofNat 1352).normalize = Case.ofNat 328 := by decide
  rw [he]
  exact case0328
#print axioms case1352

theorem case2376 : checkNat 2376 = true := by
  apply check_of_normalize (Case.ofNat 2376)
  have he : (Case.ofNat 2376).normalize = Case.ofNat 328 := by decide
  rw [he]
  exact case0328
#print axioms case2376

theorem case3400 : checkNat 3400 = true := by
  apply check_of_normalize (Case.ofNat 3400)
  have he : (Case.ofNat 3400).normalize = Case.ofNat 328 := by decide
  rw [he]
  exact case0328
#print axioms case3400

theorem case0329 : checkNat 329 = true := by native_decide
#print axioms case0329

theorem case2377 : checkNat 2377 = true := by
  apply check_of_normalize (Case.ofNat 2377)
  have he : (Case.ofNat 2377).normalize = Case.ofNat 329 := by decide
  rw [he]
  exact case0329
#print axioms case2377

theorem case0330 : checkNat 330 = true := by native_decide
#print axioms case0330

theorem case1354 : checkNat 1354 = true := by
  apply check_of_normalize (Case.ofNat 1354)
  have he : (Case.ofNat 1354).normalize = Case.ofNat 330 := by decide
  rw [he]
  exact case0330
#print axioms case1354

theorem case0331 : checkNat 331 = true := by native_decide
#print axioms case0331

theorem case0332 : checkNat 332 = true := by native_decide
#print axioms case0332

theorem case1356 : checkNat 1356 = true := by
  apply check_of_normalize (Case.ofNat 1356)
  have he : (Case.ofNat 1356).normalize = Case.ofNat 332 := by decide
  rw [he]
  exact case0332
#print axioms case1356

theorem case2380 : checkNat 2380 = true := by
  apply check_of_normalize (Case.ofNat 2380)
  have he : (Case.ofNat 2380).normalize = Case.ofNat 332 := by decide
  rw [he]
  exact case0332
#print axioms case2380

theorem case3404 : checkNat 3404 = true := by
  apply check_of_normalize (Case.ofNat 3404)
  have he : (Case.ofNat 3404).normalize = Case.ofNat 332 := by decide
  rw [he]
  exact case0332
#print axioms case3404

theorem case0333 : checkNat 333 = true := by native_decide
#print axioms case0333

theorem case2381 : checkNat 2381 = true := by
  apply check_of_normalize (Case.ofNat 2381)
  have he : (Case.ofNat 2381).normalize = Case.ofNat 333 := by decide
  rw [he]
  exact case0333
#print axioms case2381

theorem case0334 : checkNat 334 = true := by native_decide
#print axioms case0334

theorem case1358 : checkNat 1358 = true := by
  apply check_of_normalize (Case.ofNat 1358)
  have he : (Case.ofNat 1358).normalize = Case.ofNat 334 := by decide
  rw [he]
  exact case0334
#print axioms case1358

theorem case0335 : checkNat 335 = true := by native_decide
#print axioms case0335

theorem case0336 : checkNat 336 = true := by native_decide
#print axioms case0336

theorem case1360 : checkNat 1360 = true := by
  apply check_of_normalize (Case.ofNat 1360)
  have he : (Case.ofNat 1360).normalize = Case.ofNat 336 := by decide
  rw [he]
  exact case0336
#print axioms case1360

theorem case2384 : checkNat 2384 = true := by
  apply check_of_normalize (Case.ofNat 2384)
  have he : (Case.ofNat 2384).normalize = Case.ofNat 336 := by decide
  rw [he]
  exact case0336
#print axioms case2384

theorem case3408 : checkNat 3408 = true := by
  apply check_of_normalize (Case.ofNat 3408)
  have he : (Case.ofNat 3408).normalize = Case.ofNat 336 := by decide
  rw [he]
  exact case0336
#print axioms case3408

theorem case0337 : checkNat 337 = true := by native_decide
#print axioms case0337

theorem case2385 : checkNat 2385 = true := by
  apply check_of_normalize (Case.ofNat 2385)
  have he : (Case.ofNat 2385).normalize = Case.ofNat 337 := by decide
  rw [he]
  exact case0337
#print axioms case2385

theorem case0338 : checkNat 338 = true := by native_decide
#print axioms case0338

theorem case1362 : checkNat 1362 = true := by
  apply check_of_normalize (Case.ofNat 1362)
  have he : (Case.ofNat 1362).normalize = Case.ofNat 338 := by decide
  rw [he]
  exact case0338
#print axioms case1362

theorem case0339 : checkNat 339 = true := by native_decide
#print axioms case0339

theorem case0340 : checkNat 340 = true := by native_decide
#print axioms case0340

theorem case1364 : checkNat 1364 = true := by
  apply check_of_normalize (Case.ofNat 1364)
  have he : (Case.ofNat 1364).normalize = Case.ofNat 340 := by decide
  rw [he]
  exact case0340
#print axioms case1364

theorem case2388 : checkNat 2388 = true := by
  apply check_of_normalize (Case.ofNat 2388)
  have he : (Case.ofNat 2388).normalize = Case.ofNat 340 := by decide
  rw [he]
  exact case0340
#print axioms case2388

theorem case3412 : checkNat 3412 = true := by
  apply check_of_normalize (Case.ofNat 3412)
  have he : (Case.ofNat 3412).normalize = Case.ofNat 340 := by decide
  rw [he]
  exact case0340
#print axioms case3412

theorem case0341 : checkNat 341 = true := by native_decide
#print axioms case0341

theorem case2389 : checkNat 2389 = true := by
  apply check_of_normalize (Case.ofNat 2389)
  have he : (Case.ofNat 2389).normalize = Case.ofNat 341 := by decide
  rw [he]
  exact case0341
#print axioms case2389

theorem case0342 : checkNat 342 = true := by native_decide
#print axioms case0342

theorem case1366 : checkNat 1366 = true := by
  apply check_of_normalize (Case.ofNat 1366)
  have he : (Case.ofNat 1366).normalize = Case.ofNat 342 := by decide
  rw [he]
  exact case0342
#print axioms case1366

theorem case0343 : checkNat 343 = true := by native_decide
#print axioms case0343

theorem case0344 : checkNat 344 = true := by native_decide
#print axioms case0344

theorem case1368 : checkNat 1368 = true := by
  apply check_of_normalize (Case.ofNat 1368)
  have he : (Case.ofNat 1368).normalize = Case.ofNat 344 := by decide
  rw [he]
  exact case0344
#print axioms case1368

theorem case2392 : checkNat 2392 = true := by
  apply check_of_normalize (Case.ofNat 2392)
  have he : (Case.ofNat 2392).normalize = Case.ofNat 344 := by decide
  rw [he]
  exact case0344
#print axioms case2392

theorem case3416 : checkNat 3416 = true := by
  apply check_of_normalize (Case.ofNat 3416)
  have he : (Case.ofNat 3416).normalize = Case.ofNat 344 := by decide
  rw [he]
  exact case0344
#print axioms case3416

theorem case0345 : checkNat 345 = true := by native_decide
#print axioms case0345

theorem case2393 : checkNat 2393 = true := by
  apply check_of_normalize (Case.ofNat 2393)
  have he : (Case.ofNat 2393).normalize = Case.ofNat 345 := by decide
  rw [he]
  exact case0345
#print axioms case2393

theorem case0346 : checkNat 346 = true := by native_decide
#print axioms case0346

theorem case1370 : checkNat 1370 = true := by
  apply check_of_normalize (Case.ofNat 1370)
  have he : (Case.ofNat 1370).normalize = Case.ofNat 346 := by decide
  rw [he]
  exact case0346
#print axioms case1370

theorem case0347 : checkNat 347 = true := by native_decide
#print axioms case0347

theorem case0348 : checkNat 348 = true := by native_decide
#print axioms case0348

theorem case1372 : checkNat 1372 = true := by
  apply check_of_normalize (Case.ofNat 1372)
  have he : (Case.ofNat 1372).normalize = Case.ofNat 348 := by decide
  rw [he]
  exact case0348
#print axioms case1372

theorem case2396 : checkNat 2396 = true := by
  apply check_of_normalize (Case.ofNat 2396)
  have he : (Case.ofNat 2396).normalize = Case.ofNat 348 := by decide
  rw [he]
  exact case0348
#print axioms case2396

theorem case3420 : checkNat 3420 = true := by
  apply check_of_normalize (Case.ofNat 3420)
  have he : (Case.ofNat 3420).normalize = Case.ofNat 348 := by decide
  rw [he]
  exact case0348
#print axioms case3420

theorem case0349 : checkNat 349 = true := by native_decide
#print axioms case0349

theorem case2397 : checkNat 2397 = true := by
  apply check_of_normalize (Case.ofNat 2397)
  have he : (Case.ofNat 2397).normalize = Case.ofNat 349 := by decide
  rw [he]
  exact case0349
#print axioms case2397

theorem case0350 : checkNat 350 = true := by native_decide
#print axioms case0350

theorem case1374 : checkNat 1374 = true := by
  apply check_of_normalize (Case.ofNat 1374)
  have he : (Case.ofNat 1374).normalize = Case.ofNat 350 := by decide
  rw [he]
  exact case0350
#print axioms case1374

theorem case0351 : checkNat 351 = true := by native_decide
#print axioms case0351

theorem accepted :
    checkNat 320 = true ∧
    checkNat 321 = true ∧
    checkNat 322 = true ∧
    checkNat 323 = true ∧
    checkNat 324 = true ∧
    checkNat 325 = true ∧
    checkNat 326 = true ∧
    checkNat 327 = true ∧
    checkNat 328 = true ∧
    checkNat 329 = true ∧
    checkNat 330 = true ∧
    checkNat 331 = true ∧
    checkNat 332 = true ∧
    checkNat 333 = true ∧
    checkNat 334 = true ∧
    checkNat 335 = true ∧
    checkNat 336 = true ∧
    checkNat 337 = true ∧
    checkNat 338 = true ∧
    checkNat 339 = true ∧
    checkNat 340 = true ∧
    checkNat 341 = true ∧
    checkNat 342 = true ∧
    checkNat 343 = true ∧
    checkNat 344 = true ∧
    checkNat 345 = true ∧
    checkNat 346 = true ∧
    checkNat 347 = true ∧
    checkNat 348 = true ∧
    checkNat 349 = true ∧
    checkNat 350 = true ∧
    checkNat 351 = true ∧
    checkNat 1344 = true ∧
    checkNat 1346 = true ∧
    checkNat 1348 = true ∧
    checkNat 1350 = true ∧
    checkNat 1352 = true ∧
    checkNat 1354 = true ∧
    checkNat 1356 = true ∧
    checkNat 1358 = true ∧
    checkNat 1360 = true ∧
    checkNat 1362 = true ∧
    checkNat 1364 = true ∧
    checkNat 1366 = true ∧
    checkNat 1368 = true ∧
    checkNat 1370 = true ∧
    checkNat 1372 = true ∧
    checkNat 1374 = true ∧
    checkNat 2368 = true ∧
    checkNat 2369 = true ∧
    checkNat 2372 = true ∧
    checkNat 2373 = true ∧
    checkNat 2376 = true ∧
    checkNat 2377 = true ∧
    checkNat 2380 = true ∧
    checkNat 2381 = true ∧
    checkNat 2384 = true ∧
    checkNat 2385 = true ∧
    checkNat 2388 = true ∧
    checkNat 2389 = true ∧
    checkNat 2392 = true ∧
    checkNat 2393 = true ∧
    checkNat 2396 = true ∧
    checkNat 2397 = true ∧
    checkNat 3392 = true ∧
    checkNat 3396 = true ∧
    checkNat 3400 = true ∧
    checkNat 3404 = true ∧
    checkNat 3408 = true ∧
    checkNat 3412 = true ∧
    checkNat 3416 = true ∧
    checkNat 3420 = true := by
  exact ⟨case0320, case0321, case0322, case0323, case0324, case0325, case0326, case0327, case0328, case0329, case0330, case0331, case0332, case0333, case0334, case0335, case0336, case0337, case0338, case0339, case0340, case0341, case0342, case0343, case0344, case0345, case0346, case0347, case0348, case0349, case0350, case0351, case1344, case1346, case1348, case1350, case1352, case1354, case1356, case1358, case1360, case1362, case1364, case1366, case1368, case1370, case1372, case1374, case2368, case2369, case2372, case2373, case2376, case2377, case2380, case2381, case2384, case2385, case2388, case2389, case2392, case2393, case2396, case2397, case3392, case3396, case3400, case3404, case3408, case3412, case3416, case3420⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0320
