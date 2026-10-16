import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0384
open Sq19.Endgame.Reduction

theorem case0384 : checkNat 384 = true := by native_decide
#print axioms case0384

theorem case1408 : checkNat 1408 = true := by
  apply check_of_normalize (Case.ofNat 1408)
  have he : (Case.ofNat 1408).normalize = Case.ofNat 384 := by decide
  rw [he]
  exact case0384
#print axioms case1408

theorem case2432 : checkNat 2432 = true := by
  apply check_of_normalize (Case.ofNat 2432)
  have he : (Case.ofNat 2432).normalize = Case.ofNat 384 := by decide
  rw [he]
  exact case0384
#print axioms case2432

theorem case3456 : checkNat 3456 = true := by
  apply check_of_normalize (Case.ofNat 3456)
  have he : (Case.ofNat 3456).normalize = Case.ofNat 384 := by decide
  rw [he]
  exact case0384
#print axioms case3456

theorem case0385 : checkNat 385 = true := by native_decide
#print axioms case0385

theorem case2433 : checkNat 2433 = true := by
  apply check_of_normalize (Case.ofNat 2433)
  have he : (Case.ofNat 2433).normalize = Case.ofNat 385 := by decide
  rw [he]
  exact case0385
#print axioms case2433

theorem case0386 : checkNat 386 = true := by native_decide
#print axioms case0386

theorem case1410 : checkNat 1410 = true := by
  apply check_of_normalize (Case.ofNat 1410)
  have he : (Case.ofNat 1410).normalize = Case.ofNat 386 := by decide
  rw [he]
  exact case0386
#print axioms case1410

theorem case0387 : checkNat 387 = true := by native_decide
#print axioms case0387

theorem case0388 : checkNat 388 = true := by native_decide
#print axioms case0388

theorem case1412 : checkNat 1412 = true := by
  apply check_of_normalize (Case.ofNat 1412)
  have he : (Case.ofNat 1412).normalize = Case.ofNat 388 := by decide
  rw [he]
  exact case0388
#print axioms case1412

theorem case2436 : checkNat 2436 = true := by
  apply check_of_normalize (Case.ofNat 2436)
  have he : (Case.ofNat 2436).normalize = Case.ofNat 388 := by decide
  rw [he]
  exact case0388
#print axioms case2436

theorem case3460 : checkNat 3460 = true := by
  apply check_of_normalize (Case.ofNat 3460)
  have he : (Case.ofNat 3460).normalize = Case.ofNat 388 := by decide
  rw [he]
  exact case0388
#print axioms case3460

theorem case0389 : checkNat 389 = true := by native_decide
#print axioms case0389

theorem case2437 : checkNat 2437 = true := by
  apply check_of_normalize (Case.ofNat 2437)
  have he : (Case.ofNat 2437).normalize = Case.ofNat 389 := by decide
  rw [he]
  exact case0389
#print axioms case2437

theorem case0390 : checkNat 390 = true := by native_decide
#print axioms case0390

theorem case1414 : checkNat 1414 = true := by
  apply check_of_normalize (Case.ofNat 1414)
  have he : (Case.ofNat 1414).normalize = Case.ofNat 390 := by decide
  rw [he]
  exact case0390
#print axioms case1414

theorem case0391 : checkNat 391 = true := by native_decide
#print axioms case0391

theorem case0392 : checkNat 392 = true := by native_decide
#print axioms case0392

theorem case1416 : checkNat 1416 = true := by
  apply check_of_normalize (Case.ofNat 1416)
  have he : (Case.ofNat 1416).normalize = Case.ofNat 392 := by decide
  rw [he]
  exact case0392
#print axioms case1416

theorem case2440 : checkNat 2440 = true := by
  apply check_of_normalize (Case.ofNat 2440)
  have he : (Case.ofNat 2440).normalize = Case.ofNat 392 := by decide
  rw [he]
  exact case0392
#print axioms case2440

theorem case3464 : checkNat 3464 = true := by
  apply check_of_normalize (Case.ofNat 3464)
  have he : (Case.ofNat 3464).normalize = Case.ofNat 392 := by decide
  rw [he]
  exact case0392
#print axioms case3464

theorem case0393 : checkNat 393 = true := by native_decide
#print axioms case0393

theorem case2441 : checkNat 2441 = true := by
  apply check_of_normalize (Case.ofNat 2441)
  have he : (Case.ofNat 2441).normalize = Case.ofNat 393 := by decide
  rw [he]
  exact case0393
#print axioms case2441

theorem case0394 : checkNat 394 = true := by native_decide
#print axioms case0394

theorem case1418 : checkNat 1418 = true := by
  apply check_of_normalize (Case.ofNat 1418)
  have he : (Case.ofNat 1418).normalize = Case.ofNat 394 := by decide
  rw [he]
  exact case0394
#print axioms case1418

theorem case0395 : checkNat 395 = true := by native_decide
#print axioms case0395

theorem case0396 : checkNat 396 = true := by native_decide
#print axioms case0396

theorem case1420 : checkNat 1420 = true := by
  apply check_of_normalize (Case.ofNat 1420)
  have he : (Case.ofNat 1420).normalize = Case.ofNat 396 := by decide
  rw [he]
  exact case0396
#print axioms case1420

theorem case2444 : checkNat 2444 = true := by
  apply check_of_normalize (Case.ofNat 2444)
  have he : (Case.ofNat 2444).normalize = Case.ofNat 396 := by decide
  rw [he]
  exact case0396
#print axioms case2444

theorem case3468 : checkNat 3468 = true := by
  apply check_of_normalize (Case.ofNat 3468)
  have he : (Case.ofNat 3468).normalize = Case.ofNat 396 := by decide
  rw [he]
  exact case0396
#print axioms case3468

theorem case0397 : checkNat 397 = true := by native_decide
#print axioms case0397

theorem case2445 : checkNat 2445 = true := by
  apply check_of_normalize (Case.ofNat 2445)
  have he : (Case.ofNat 2445).normalize = Case.ofNat 397 := by decide
  rw [he]
  exact case0397
#print axioms case2445

theorem case0398 : checkNat 398 = true := by native_decide
#print axioms case0398

theorem case1422 : checkNat 1422 = true := by
  apply check_of_normalize (Case.ofNat 1422)
  have he : (Case.ofNat 1422).normalize = Case.ofNat 398 := by decide
  rw [he]
  exact case0398
#print axioms case1422

theorem case0399 : checkNat 399 = true := by native_decide
#print axioms case0399

theorem case0400 : checkNat 400 = true := by native_decide
#print axioms case0400

theorem case1424 : checkNat 1424 = true := by
  apply check_of_normalize (Case.ofNat 1424)
  have he : (Case.ofNat 1424).normalize = Case.ofNat 400 := by decide
  rw [he]
  exact case0400
#print axioms case1424

theorem case2448 : checkNat 2448 = true := by
  apply check_of_normalize (Case.ofNat 2448)
  have he : (Case.ofNat 2448).normalize = Case.ofNat 400 := by decide
  rw [he]
  exact case0400
#print axioms case2448

theorem case3472 : checkNat 3472 = true := by
  apply check_of_normalize (Case.ofNat 3472)
  have he : (Case.ofNat 3472).normalize = Case.ofNat 400 := by decide
  rw [he]
  exact case0400
#print axioms case3472

theorem case0401 : checkNat 401 = true := by native_decide
#print axioms case0401

theorem case2449 : checkNat 2449 = true := by
  apply check_of_normalize (Case.ofNat 2449)
  have he : (Case.ofNat 2449).normalize = Case.ofNat 401 := by decide
  rw [he]
  exact case0401
#print axioms case2449

theorem case0402 : checkNat 402 = true := by native_decide
#print axioms case0402

theorem case1426 : checkNat 1426 = true := by
  apply check_of_normalize (Case.ofNat 1426)
  have he : (Case.ofNat 1426).normalize = Case.ofNat 402 := by decide
  rw [he]
  exact case0402
#print axioms case1426

theorem case0403 : checkNat 403 = true := by native_decide
#print axioms case0403

theorem case0404 : checkNat 404 = true := by native_decide
#print axioms case0404

theorem case1428 : checkNat 1428 = true := by
  apply check_of_normalize (Case.ofNat 1428)
  have he : (Case.ofNat 1428).normalize = Case.ofNat 404 := by decide
  rw [he]
  exact case0404
#print axioms case1428

theorem case2452 : checkNat 2452 = true := by
  apply check_of_normalize (Case.ofNat 2452)
  have he : (Case.ofNat 2452).normalize = Case.ofNat 404 := by decide
  rw [he]
  exact case0404
#print axioms case2452

theorem case3476 : checkNat 3476 = true := by
  apply check_of_normalize (Case.ofNat 3476)
  have he : (Case.ofNat 3476).normalize = Case.ofNat 404 := by decide
  rw [he]
  exact case0404
#print axioms case3476

theorem case0405 : checkNat 405 = true := by native_decide
#print axioms case0405

theorem case2453 : checkNat 2453 = true := by
  apply check_of_normalize (Case.ofNat 2453)
  have he : (Case.ofNat 2453).normalize = Case.ofNat 405 := by decide
  rw [he]
  exact case0405
#print axioms case2453

theorem case0406 : checkNat 406 = true := by native_decide
#print axioms case0406

theorem case1430 : checkNat 1430 = true := by
  apply check_of_normalize (Case.ofNat 1430)
  have he : (Case.ofNat 1430).normalize = Case.ofNat 406 := by decide
  rw [he]
  exact case0406
#print axioms case1430

theorem case0407 : checkNat 407 = true := by native_decide
#print axioms case0407

theorem case0408 : checkNat 408 = true := by native_decide
#print axioms case0408

theorem case1432 : checkNat 1432 = true := by
  apply check_of_normalize (Case.ofNat 1432)
  have he : (Case.ofNat 1432).normalize = Case.ofNat 408 := by decide
  rw [he]
  exact case0408
#print axioms case1432

theorem case2456 : checkNat 2456 = true := by
  apply check_of_normalize (Case.ofNat 2456)
  have he : (Case.ofNat 2456).normalize = Case.ofNat 408 := by decide
  rw [he]
  exact case0408
#print axioms case2456

theorem case3480 : checkNat 3480 = true := by
  apply check_of_normalize (Case.ofNat 3480)
  have he : (Case.ofNat 3480).normalize = Case.ofNat 408 := by decide
  rw [he]
  exact case0408
#print axioms case3480

theorem case0409 : checkNat 409 = true := by native_decide
#print axioms case0409

theorem case2457 : checkNat 2457 = true := by
  apply check_of_normalize (Case.ofNat 2457)
  have he : (Case.ofNat 2457).normalize = Case.ofNat 409 := by decide
  rw [he]
  exact case0409
#print axioms case2457

theorem case0410 : checkNat 410 = true := by native_decide
#print axioms case0410

theorem case1434 : checkNat 1434 = true := by
  apply check_of_normalize (Case.ofNat 1434)
  have he : (Case.ofNat 1434).normalize = Case.ofNat 410 := by decide
  rw [he]
  exact case0410
#print axioms case1434

theorem case0411 : checkNat 411 = true := by native_decide
#print axioms case0411

theorem case0412 : checkNat 412 = true := by native_decide
#print axioms case0412

theorem case1436 : checkNat 1436 = true := by
  apply check_of_normalize (Case.ofNat 1436)
  have he : (Case.ofNat 1436).normalize = Case.ofNat 412 := by decide
  rw [he]
  exact case0412
#print axioms case1436

theorem case2460 : checkNat 2460 = true := by
  apply check_of_normalize (Case.ofNat 2460)
  have he : (Case.ofNat 2460).normalize = Case.ofNat 412 := by decide
  rw [he]
  exact case0412
#print axioms case2460

theorem case3484 : checkNat 3484 = true := by
  apply check_of_normalize (Case.ofNat 3484)
  have he : (Case.ofNat 3484).normalize = Case.ofNat 412 := by decide
  rw [he]
  exact case0412
#print axioms case3484

theorem case0413 : checkNat 413 = true := by native_decide
#print axioms case0413

theorem case2461 : checkNat 2461 = true := by
  apply check_of_normalize (Case.ofNat 2461)
  have he : (Case.ofNat 2461).normalize = Case.ofNat 413 := by decide
  rw [he]
  exact case0413
#print axioms case2461

theorem case0414 : checkNat 414 = true := by native_decide
#print axioms case0414

theorem case1438 : checkNat 1438 = true := by
  apply check_of_normalize (Case.ofNat 1438)
  have he : (Case.ofNat 1438).normalize = Case.ofNat 414 := by decide
  rw [he]
  exact case0414
#print axioms case1438

theorem case0415 : checkNat 415 = true := by native_decide
#print axioms case0415

theorem accepted :
    checkNat 384 = true ∧
    checkNat 385 = true ∧
    checkNat 386 = true ∧
    checkNat 387 = true ∧
    checkNat 388 = true ∧
    checkNat 389 = true ∧
    checkNat 390 = true ∧
    checkNat 391 = true ∧
    checkNat 392 = true ∧
    checkNat 393 = true ∧
    checkNat 394 = true ∧
    checkNat 395 = true ∧
    checkNat 396 = true ∧
    checkNat 397 = true ∧
    checkNat 398 = true ∧
    checkNat 399 = true ∧
    checkNat 400 = true ∧
    checkNat 401 = true ∧
    checkNat 402 = true ∧
    checkNat 403 = true ∧
    checkNat 404 = true ∧
    checkNat 405 = true ∧
    checkNat 406 = true ∧
    checkNat 407 = true ∧
    checkNat 408 = true ∧
    checkNat 409 = true ∧
    checkNat 410 = true ∧
    checkNat 411 = true ∧
    checkNat 412 = true ∧
    checkNat 413 = true ∧
    checkNat 414 = true ∧
    checkNat 415 = true ∧
    checkNat 1408 = true ∧
    checkNat 1410 = true ∧
    checkNat 1412 = true ∧
    checkNat 1414 = true ∧
    checkNat 1416 = true ∧
    checkNat 1418 = true ∧
    checkNat 1420 = true ∧
    checkNat 1422 = true ∧
    checkNat 1424 = true ∧
    checkNat 1426 = true ∧
    checkNat 1428 = true ∧
    checkNat 1430 = true ∧
    checkNat 1432 = true ∧
    checkNat 1434 = true ∧
    checkNat 1436 = true ∧
    checkNat 1438 = true ∧
    checkNat 2432 = true ∧
    checkNat 2433 = true ∧
    checkNat 2436 = true ∧
    checkNat 2437 = true ∧
    checkNat 2440 = true ∧
    checkNat 2441 = true ∧
    checkNat 2444 = true ∧
    checkNat 2445 = true ∧
    checkNat 2448 = true ∧
    checkNat 2449 = true ∧
    checkNat 2452 = true ∧
    checkNat 2453 = true ∧
    checkNat 2456 = true ∧
    checkNat 2457 = true ∧
    checkNat 2460 = true ∧
    checkNat 2461 = true ∧
    checkNat 3456 = true ∧
    checkNat 3460 = true ∧
    checkNat 3464 = true ∧
    checkNat 3468 = true ∧
    checkNat 3472 = true ∧
    checkNat 3476 = true ∧
    checkNat 3480 = true ∧
    checkNat 3484 = true := by
  exact ⟨case0384, case0385, case0386, case0387, case0388, case0389, case0390, case0391, case0392, case0393, case0394, case0395, case0396, case0397, case0398, case0399, case0400, case0401, case0402, case0403, case0404, case0405, case0406, case0407, case0408, case0409, case0410, case0411, case0412, case0413, case0414, case0415, case1408, case1410, case1412, case1414, case1416, case1418, case1420, case1422, case1424, case1426, case1428, case1430, case1432, case1434, case1436, case1438, case2432, case2433, case2436, case2437, case2440, case2441, case2444, case2445, case2448, case2449, case2452, case2453, case2456, case2457, case2460, case2461, case3456, case3460, case3464, case3468, case3472, case3476, case3480, case3484⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0384
