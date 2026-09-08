import SquarePackingArchive.QuadraticCertificate
import Mathlib.Tactic.FinCases

namespace SquarePackingArchive.Records.Square26Tracker

def certificate : QuadraticCertificate 2 26 where
  side := { rational := ((7 : ℚ) / 2), radical := ((3 : ℚ) / 2) }
  squares := #v[
    { centerX := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, centerY := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := ((3 : ℚ) / 2), radical := (0 : ℚ) }, centerY := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, centerY := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (1 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, centerY := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := ((3 : ℚ) / 2), radical := (0 : ℚ) }, centerY := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, centerY := { rational := ((3 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (1 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (2 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := ((3 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := ((1 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := ((3 : ℚ) / 2), radical := (0 : ℚ) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := (3 : ℚ), radical := ((3 : ℚ) / 2) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, cosine := { rational := (1 : ℚ), radical := (0 : ℚ) }, sine := { rational := (0 : ℚ), radical := (0 : ℚ) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((7 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((5 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((5 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((7 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((1 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((5 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((5 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((1 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((-1 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((1 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((1 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } },
    { centerX := { rational := ((5 : ℚ) / 4), radical := ((3 : ℚ) / 4) }, centerY := { rational := ((7 : ℚ) / 4), radical := ((-1 : ℚ) / 4) }, cosine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) }, sine := { rational := (0 : ℚ), radical := ((1 : ℚ) / 2) } }
  ]
  separatingAxes := #v[
    #v[.leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .rightVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftVertical, .leftVertical, .leftVertical],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .rightVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .rightHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .rightHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftVertical, .leftVertical, .rightHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .rightHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftVertical, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .rightVertical],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .rightVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical, .leftVertical],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftVertical],
    #v[.leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal, .leftHorizontal]
  ]

set_option Elab.async false
set_option maxHeartbeats 0
set_option maxRecDepth 100000

private theorem boundaries_valid : certificate.BoundariesValid := by decide +kernel

private theorem separated_row_0 : certificate.SeparatedRow 0 := by decide +kernel

private theorem separated_row_1 : certificate.SeparatedRow 1 := by decide +kernel

private theorem separated_row_2 : certificate.SeparatedRow 2 := by decide +kernel

private theorem separated_row_3 : certificate.SeparatedRow 3 := by decide +kernel

private theorem separated_row_4 : certificate.SeparatedRow 4 := by decide +kernel

private theorem separated_row_5 : certificate.SeparatedRow 5 := by decide +kernel

private theorem separated_row_6 : certificate.SeparatedRow 6 := by decide +kernel

private theorem separated_row_7 : certificate.SeparatedRow 7 := by decide +kernel

private theorem separated_row_8 : certificate.SeparatedRow 8 := by decide +kernel

private theorem separated_row_9 : certificate.SeparatedRow 9 := by decide +kernel

private theorem separated_row_10 : certificate.SeparatedRow 10 := by decide +kernel

private theorem separated_row_11 : certificate.SeparatedRow 11 := by decide +kernel

private theorem separated_row_12 : certificate.SeparatedRow 12 := by decide +kernel

private theorem separated_row_13 : certificate.SeparatedRow 13 := by decide +kernel

private theorem separated_row_14 : certificate.SeparatedRow 14 := by decide +kernel

private theorem separated_row_15 : certificate.SeparatedRow 15 := by decide +kernel

private theorem separated_row_16 : certificate.SeparatedRow 16 := by decide +kernel

private theorem separated_row_17 : certificate.SeparatedRow 17 := by decide +kernel

private theorem separated_row_18 : certificate.SeparatedRow 18 := by decide +kernel

private theorem separated_row_19 : certificate.SeparatedRow 19 := by decide +kernel

private theorem separated_row_20 : certificate.SeparatedRow 20 := by decide +kernel

private theorem separated_row_21 : certificate.SeparatedRow 21 := by decide +kernel

private theorem separated_row_22 : certificate.SeparatedRow 22 := by decide +kernel

private theorem separated_row_23 : certificate.SeparatedRow 23 := by decide +kernel

private theorem separated_row_24 : certificate.SeparatedRow 24 := by decide +kernel

private theorem separated_row_25 : certificate.SeparatedRow 25 := by decide +kernel

theorem certificate_valid : certificate.Valid := by
  apply QuadraticCertificate.valid_of_rows boundaries_valid
  intro left
  fin_cases left
  · exact separated_row_0
  · exact separated_row_1
  · exact separated_row_2
  · exact separated_row_3
  · exact separated_row_4
  · exact separated_row_5
  · exact separated_row_6
  · exact separated_row_7
  · exact separated_row_8
  · exact separated_row_9
  · exact separated_row_10
  · exact separated_row_11
  · exact separated_row_12
  · exact separated_row_13
  · exact separated_row_14
  · exact separated_row_15
  · exact separated_row_16
  · exact separated_row_17
  · exact separated_row_18
  · exact separated_row_19
  · exact separated_row_20
  · exact separated_row_21
  · exact separated_row_22
  · exact separated_row_23
  · exact separated_row_24
  · exact separated_row_25

theorem upper_bound : HasPacking 26 ((((7 : ℚ) / 2) : ℝ) + (((3 : ℚ) / 2) : ℝ) * Real.sqrt 2) := by
  simpa [certificate, QuadraticNumber.toReal] using QuadraticCertificate.valid_sound certificate_valid

end SquarePackingArchive.Records.Square26Tracker
