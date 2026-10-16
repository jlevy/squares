import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0416
open Sq19.Endgame.Reduction

theorem case0416 : checkNat 416 = true := by native_decide
#print axioms case0416

theorem case1440 : checkNat 1440 = true := by
  apply check_of_normalize (Case.ofNat 1440)
  have he : (Case.ofNat 1440).normalize = Case.ofNat 416 := by decide
  rw [he]
  exact case0416
#print axioms case1440

theorem case2464 : checkNat 2464 = true := by
  apply check_of_normalize (Case.ofNat 2464)
  have he : (Case.ofNat 2464).normalize = Case.ofNat 416 := by decide
  rw [he]
  exact case0416
#print axioms case2464

theorem case3488 : checkNat 3488 = true := by
  apply check_of_normalize (Case.ofNat 3488)
  have he : (Case.ofNat 3488).normalize = Case.ofNat 416 := by decide
  rw [he]
  exact case0416
#print axioms case3488

theorem case0417 : checkNat 417 = true := by native_decide
#print axioms case0417

theorem case2465 : checkNat 2465 = true := by
  apply check_of_normalize (Case.ofNat 2465)
  have he : (Case.ofNat 2465).normalize = Case.ofNat 417 := by decide
  rw [he]
  exact case0417
#print axioms case2465

theorem case0418 : checkNat 418 = true := by native_decide
#print axioms case0418

theorem case1442 : checkNat 1442 = true := by
  apply check_of_normalize (Case.ofNat 1442)
  have he : (Case.ofNat 1442).normalize = Case.ofNat 418 := by decide
  rw [he]
  exact case0418
#print axioms case1442

theorem case0419 : checkNat 419 = true := by native_decide
#print axioms case0419

theorem case0420 : checkNat 420 = true := by native_decide
#print axioms case0420

theorem case1444 : checkNat 1444 = true := by
  apply check_of_normalize (Case.ofNat 1444)
  have he : (Case.ofNat 1444).normalize = Case.ofNat 420 := by decide
  rw [he]
  exact case0420
#print axioms case1444

theorem case2468 : checkNat 2468 = true := by
  apply check_of_normalize (Case.ofNat 2468)
  have he : (Case.ofNat 2468).normalize = Case.ofNat 420 := by decide
  rw [he]
  exact case0420
#print axioms case2468

theorem case3492 : checkNat 3492 = true := by
  apply check_of_normalize (Case.ofNat 3492)
  have he : (Case.ofNat 3492).normalize = Case.ofNat 420 := by decide
  rw [he]
  exact case0420
#print axioms case3492

theorem case0421 : checkNat 421 = true := by native_decide
#print axioms case0421

theorem case2469 : checkNat 2469 = true := by
  apply check_of_normalize (Case.ofNat 2469)
  have he : (Case.ofNat 2469).normalize = Case.ofNat 421 := by decide
  rw [he]
  exact case0421
#print axioms case2469

theorem case0422 : checkNat 422 = true := by native_decide
#print axioms case0422

theorem case1446 : checkNat 1446 = true := by
  apply check_of_normalize (Case.ofNat 1446)
  have he : (Case.ofNat 1446).normalize = Case.ofNat 422 := by decide
  rw [he]
  exact case0422
#print axioms case1446

theorem case0423 : checkNat 423 = true := by native_decide
#print axioms case0423

theorem case0424 : checkNat 424 = true := by native_decide
#print axioms case0424

theorem case1448 : checkNat 1448 = true := by
  apply check_of_normalize (Case.ofNat 1448)
  have he : (Case.ofNat 1448).normalize = Case.ofNat 424 := by decide
  rw [he]
  exact case0424
#print axioms case1448

theorem case2472 : checkNat 2472 = true := by
  apply check_of_normalize (Case.ofNat 2472)
  have he : (Case.ofNat 2472).normalize = Case.ofNat 424 := by decide
  rw [he]
  exact case0424
#print axioms case2472

theorem case3496 : checkNat 3496 = true := by
  apply check_of_normalize (Case.ofNat 3496)
  have he : (Case.ofNat 3496).normalize = Case.ofNat 424 := by decide
  rw [he]
  exact case0424
#print axioms case3496

theorem case0425 : checkNat 425 = true := by native_decide
#print axioms case0425

theorem case2473 : checkNat 2473 = true := by
  apply check_of_normalize (Case.ofNat 2473)
  have he : (Case.ofNat 2473).normalize = Case.ofNat 425 := by decide
  rw [he]
  exact case0425
#print axioms case2473

theorem case0426 : checkNat 426 = true := by native_decide
#print axioms case0426

theorem case1450 : checkNat 1450 = true := by
  apply check_of_normalize (Case.ofNat 1450)
  have he : (Case.ofNat 1450).normalize = Case.ofNat 426 := by decide
  rw [he]
  exact case0426
#print axioms case1450

theorem case0427 : checkNat 427 = true := by native_decide
#print axioms case0427

theorem case0428 : checkNat 428 = true := by native_decide
#print axioms case0428

theorem case1452 : checkNat 1452 = true := by
  apply check_of_normalize (Case.ofNat 1452)
  have he : (Case.ofNat 1452).normalize = Case.ofNat 428 := by decide
  rw [he]
  exact case0428
#print axioms case1452

theorem case2476 : checkNat 2476 = true := by
  apply check_of_normalize (Case.ofNat 2476)
  have he : (Case.ofNat 2476).normalize = Case.ofNat 428 := by decide
  rw [he]
  exact case0428
#print axioms case2476

theorem case3500 : checkNat 3500 = true := by
  apply check_of_normalize (Case.ofNat 3500)
  have he : (Case.ofNat 3500).normalize = Case.ofNat 428 := by decide
  rw [he]
  exact case0428
#print axioms case3500

theorem case0429 : checkNat 429 = true := by native_decide
#print axioms case0429

theorem case2477 : checkNat 2477 = true := by
  apply check_of_normalize (Case.ofNat 2477)
  have he : (Case.ofNat 2477).normalize = Case.ofNat 429 := by decide
  rw [he]
  exact case0429
#print axioms case2477

theorem case0430 : checkNat 430 = true := by native_decide
#print axioms case0430

theorem case1454 : checkNat 1454 = true := by
  apply check_of_normalize (Case.ofNat 1454)
  have he : (Case.ofNat 1454).normalize = Case.ofNat 430 := by decide
  rw [he]
  exact case0430
#print axioms case1454

theorem case0431 : checkNat 431 = true := by native_decide
#print axioms case0431

theorem case0432 : checkNat 432 = true := by native_decide
#print axioms case0432

theorem case1456 : checkNat 1456 = true := by
  apply check_of_normalize (Case.ofNat 1456)
  have he : (Case.ofNat 1456).normalize = Case.ofNat 432 := by decide
  rw [he]
  exact case0432
#print axioms case1456

theorem case2480 : checkNat 2480 = true := by
  apply check_of_normalize (Case.ofNat 2480)
  have he : (Case.ofNat 2480).normalize = Case.ofNat 432 := by decide
  rw [he]
  exact case0432
#print axioms case2480

theorem case3504 : checkNat 3504 = true := by
  apply check_of_normalize (Case.ofNat 3504)
  have he : (Case.ofNat 3504).normalize = Case.ofNat 432 := by decide
  rw [he]
  exact case0432
#print axioms case3504

theorem case0433 : checkNat 433 = true := by native_decide
#print axioms case0433

theorem case2481 : checkNat 2481 = true := by
  apply check_of_normalize (Case.ofNat 2481)
  have he : (Case.ofNat 2481).normalize = Case.ofNat 433 := by decide
  rw [he]
  exact case0433
#print axioms case2481

theorem case0434 : checkNat 434 = true := by native_decide
#print axioms case0434

theorem case1458 : checkNat 1458 = true := by
  apply check_of_normalize (Case.ofNat 1458)
  have he : (Case.ofNat 1458).normalize = Case.ofNat 434 := by decide
  rw [he]
  exact case0434
#print axioms case1458

theorem case0435 : checkNat 435 = true := by native_decide
#print axioms case0435

theorem case0436 : checkNat 436 = true := by native_decide
#print axioms case0436

theorem case1460 : checkNat 1460 = true := by
  apply check_of_normalize (Case.ofNat 1460)
  have he : (Case.ofNat 1460).normalize = Case.ofNat 436 := by decide
  rw [he]
  exact case0436
#print axioms case1460

theorem case2484 : checkNat 2484 = true := by
  apply check_of_normalize (Case.ofNat 2484)
  have he : (Case.ofNat 2484).normalize = Case.ofNat 436 := by decide
  rw [he]
  exact case0436
#print axioms case2484

theorem case3508 : checkNat 3508 = true := by
  apply check_of_normalize (Case.ofNat 3508)
  have he : (Case.ofNat 3508).normalize = Case.ofNat 436 := by decide
  rw [he]
  exact case0436
#print axioms case3508

theorem case0437 : checkNat 437 = true := by native_decide
#print axioms case0437

theorem case2485 : checkNat 2485 = true := by
  apply check_of_normalize (Case.ofNat 2485)
  have he : (Case.ofNat 2485).normalize = Case.ofNat 437 := by decide
  rw [he]
  exact case0437
#print axioms case2485

theorem case0438 : checkNat 438 = true := by native_decide
#print axioms case0438

theorem case1462 : checkNat 1462 = true := by
  apply check_of_normalize (Case.ofNat 1462)
  have he : (Case.ofNat 1462).normalize = Case.ofNat 438 := by decide
  rw [he]
  exact case0438
#print axioms case1462

theorem case0439 : checkNat 439 = true := by native_decide
#print axioms case0439

theorem case0440 : checkNat 440 = true := by native_decide
#print axioms case0440

theorem case1464 : checkNat 1464 = true := by
  apply check_of_normalize (Case.ofNat 1464)
  have he : (Case.ofNat 1464).normalize = Case.ofNat 440 := by decide
  rw [he]
  exact case0440
#print axioms case1464

theorem case2488 : checkNat 2488 = true := by
  apply check_of_normalize (Case.ofNat 2488)
  have he : (Case.ofNat 2488).normalize = Case.ofNat 440 := by decide
  rw [he]
  exact case0440
#print axioms case2488

theorem case3512 : checkNat 3512 = true := by
  apply check_of_normalize (Case.ofNat 3512)
  have he : (Case.ofNat 3512).normalize = Case.ofNat 440 := by decide
  rw [he]
  exact case0440
#print axioms case3512

theorem case0441 : checkNat 441 = true := by native_decide
#print axioms case0441

theorem case2489 : checkNat 2489 = true := by
  apply check_of_normalize (Case.ofNat 2489)
  have he : (Case.ofNat 2489).normalize = Case.ofNat 441 := by decide
  rw [he]
  exact case0441
#print axioms case2489

theorem case0442 : checkNat 442 = true := by native_decide
#print axioms case0442

theorem case1466 : checkNat 1466 = true := by
  apply check_of_normalize (Case.ofNat 1466)
  have he : (Case.ofNat 1466).normalize = Case.ofNat 442 := by decide
  rw [he]
  exact case0442
#print axioms case1466

theorem case0443 : checkNat 443 = true := by native_decide
#print axioms case0443

theorem case0444 : checkNat 444 = true := by native_decide
#print axioms case0444

theorem case1468 : checkNat 1468 = true := by
  apply check_of_normalize (Case.ofNat 1468)
  have he : (Case.ofNat 1468).normalize = Case.ofNat 444 := by decide
  rw [he]
  exact case0444
#print axioms case1468

theorem case2492 : checkNat 2492 = true := by
  apply check_of_normalize (Case.ofNat 2492)
  have he : (Case.ofNat 2492).normalize = Case.ofNat 444 := by decide
  rw [he]
  exact case0444
#print axioms case2492

theorem case3516 : checkNat 3516 = true := by
  apply check_of_normalize (Case.ofNat 3516)
  have he : (Case.ofNat 3516).normalize = Case.ofNat 444 := by decide
  rw [he]
  exact case0444
#print axioms case3516

theorem case0445 : checkNat 445 = true := by native_decide
#print axioms case0445

theorem case2493 : checkNat 2493 = true := by
  apply check_of_normalize (Case.ofNat 2493)
  have he : (Case.ofNat 2493).normalize = Case.ofNat 445 := by decide
  rw [he]
  exact case0445
#print axioms case2493

theorem case0446 : checkNat 446 = true := by native_decide
#print axioms case0446

theorem case1470 : checkNat 1470 = true := by
  apply check_of_normalize (Case.ofNat 1470)
  have he : (Case.ofNat 1470).normalize = Case.ofNat 446 := by decide
  rw [he]
  exact case0446
#print axioms case1470

theorem case0447 : checkNat 447 = true := by native_decide
#print axioms case0447

theorem accepted :
    checkNat 416 = true ∧
    checkNat 417 = true ∧
    checkNat 418 = true ∧
    checkNat 419 = true ∧
    checkNat 420 = true ∧
    checkNat 421 = true ∧
    checkNat 422 = true ∧
    checkNat 423 = true ∧
    checkNat 424 = true ∧
    checkNat 425 = true ∧
    checkNat 426 = true ∧
    checkNat 427 = true ∧
    checkNat 428 = true ∧
    checkNat 429 = true ∧
    checkNat 430 = true ∧
    checkNat 431 = true ∧
    checkNat 432 = true ∧
    checkNat 433 = true ∧
    checkNat 434 = true ∧
    checkNat 435 = true ∧
    checkNat 436 = true ∧
    checkNat 437 = true ∧
    checkNat 438 = true ∧
    checkNat 439 = true ∧
    checkNat 440 = true ∧
    checkNat 441 = true ∧
    checkNat 442 = true ∧
    checkNat 443 = true ∧
    checkNat 444 = true ∧
    checkNat 445 = true ∧
    checkNat 446 = true ∧
    checkNat 447 = true ∧
    checkNat 1440 = true ∧
    checkNat 1442 = true ∧
    checkNat 1444 = true ∧
    checkNat 1446 = true ∧
    checkNat 1448 = true ∧
    checkNat 1450 = true ∧
    checkNat 1452 = true ∧
    checkNat 1454 = true ∧
    checkNat 1456 = true ∧
    checkNat 1458 = true ∧
    checkNat 1460 = true ∧
    checkNat 1462 = true ∧
    checkNat 1464 = true ∧
    checkNat 1466 = true ∧
    checkNat 1468 = true ∧
    checkNat 1470 = true ∧
    checkNat 2464 = true ∧
    checkNat 2465 = true ∧
    checkNat 2468 = true ∧
    checkNat 2469 = true ∧
    checkNat 2472 = true ∧
    checkNat 2473 = true ∧
    checkNat 2476 = true ∧
    checkNat 2477 = true ∧
    checkNat 2480 = true ∧
    checkNat 2481 = true ∧
    checkNat 2484 = true ∧
    checkNat 2485 = true ∧
    checkNat 2488 = true ∧
    checkNat 2489 = true ∧
    checkNat 2492 = true ∧
    checkNat 2493 = true ∧
    checkNat 3488 = true ∧
    checkNat 3492 = true ∧
    checkNat 3496 = true ∧
    checkNat 3500 = true ∧
    checkNat 3504 = true ∧
    checkNat 3508 = true ∧
    checkNat 3512 = true ∧
    checkNat 3516 = true := by
  exact ⟨case0416, case0417, case0418, case0419, case0420, case0421, case0422, case0423, case0424, case0425, case0426, case0427, case0428, case0429, case0430, case0431, case0432, case0433, case0434, case0435, case0436, case0437, case0438, case0439, case0440, case0441, case0442, case0443, case0444, case0445, case0446, case0447, case1440, case1442, case1444, case1446, case1448, case1450, case1452, case1454, case1456, case1458, case1460, case1462, case1464, case1466, case1468, case1470, case2464, case2465, case2468, case2469, case2472, case2473, case2476, case2477, case2480, case2481, case2484, case2485, case2488, case2489, case2492, case2493, case3488, case3492, case3496, case3500, case3504, case3508, case3512, case3516⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0416
