// The globals `test_pdf_math_browser`'s probes install and read.

/** One wait kpress's math runtime records while it holds a face request. */
interface KpressMathFaceWait {
  request: string;
  outcome: string;
}

declare var kpressMathFaceWait: KpressMathFaceWait[] | undefined;
/** `font_fault`: the TeX source of the formula the fault was injected into. */
declare var pdfMathFaultSource: string | undefined;
/** `guard_fixture`: pristine copies of one printed `.tex` and one native formula. */
declare var pdfMathGuardNodes: { tex: Node; native: Node } | undefined;
/** `guard_fixture`: refills the fixture with a fresh copy and returns it. */
declare function resetPdfMathGuardNode(kind: "tex" | "native"): HTMLElement;
