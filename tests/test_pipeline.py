from checkout_sentinel.ci_agent import evaluate_build


def test_ci_fails_bad_candidate_and_passes_repair():
    assert evaluate_build({"free_shipping_threshold": 0})["status"] == "FAIL"
    assert evaluate_build({"free_shipping_threshold": 50})["status"] == "PASS"

