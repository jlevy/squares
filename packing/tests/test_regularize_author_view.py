"""The published n304 view is the reviewed author certificate at the same exact side."""

from devtools import regularize_author_view as author
from devtools import regularize_axis_components as axis
from devtools import regularize_evand as driver
from devtools import render_regularized_atlas as drawings


def test_author_view_keeps_its_source_geometry_and_credit() -> None:
    entry = next(item for item in drawings.regularized_entries() if item["n"] == author.N)
    assert entry["generator"] == axis.EVAND_AUTHOR_GENERATOR
    assert entry["run"] == {"id": author.RUN, "output": author.OUTPUT}
    assert entry["side"]["relation"] == "same"
    assert entry["regularization"]["by"] == axis.EVAND_AUTHOR_SOURCE_KEY
    assert entry["decision"]["row"] == axis.ADMITTING_ROW
    assert entry["exact_verification"]["half_angle"] is True
    view = drawings.view_witness(entry)
    assert view["certificate"]["credit"] == axis.EVAND_AUTHOR_CREDIT
    assert not author.source_problems(author.REPO, view)
    view["squares"][0]["center"][0] = "0"
    assert author.source_problems(author.REPO, view) == [
        "n=304: author view changes the certificate's squares"
    ]


def test_admission_receipt_records_both_exact_routes_and_every_visual_gain() -> None:
    receipt = driver.read_json(author.REPO / author.RECEIPT)
    assert receipt["run"]["parameters"]["admission_receipt"] == author.RECEIPT.as_posix()
    for route in ("repository_verifier", "independent_checker"):
        check = receipt["fresh_gmp_checks"][route]
        assert check["verification_passed"]
        assert check["pairs_tested"] == 46_056
        assert check["side"] == receipt["side"]["view"]
    half_angle = receipt["half_angle_check"]
    assert half_angle["passed"]
    assert half_angle["pairs"] == 46_056
    assert half_angle["side"] == receipt["side"]["view"]
    comparison = receipt["comparison"]
    assert len(comparison["gains"]) == 7
    assert not comparison["losses"]
    assert not receipt["contacts"]["regressions"]
    assert not receipt["contacts"]["against_current"]["regressions"]
