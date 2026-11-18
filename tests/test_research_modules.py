from veriresume.semantic import compare_claim_evidence
from veriresume.llm_reasoning import reason_about_claim

def test_tfidf_semantic_baseline_runs():
    r=compare_claim_evidence("Improved API latency by 20 percent", "Reduced API response time by 20%")
    assert r["tfidf_status"] == "computed"
    assert 0 <= r["tfidf_cosine"] <= 1
    assert "caution" in r

def test_llm_offline_returns_advisory_error():
    r=reason_about_claim("Claim example", model="model-that-does-not-exist", host="http://127.0.0.1:1")
    assert "error" in r
    assert "advisory_warning" in r
