from veriresume.analyzer import analyze_resume, extract_claims

def test_extracts_certification_and_education():
    text = "B.Tech Computer Science, Example University\nAWS Certified Solutions Architect"
    claims = extract_claims(text)
    kinds = {c["type"] for c in claims}
    assert "Education" in kinds
    assert "Certification" in kinds

def test_reversed_timeline_flagged():
    result = analyze_resume("Engineer\nJan 2024 - Jan 2021")
    assert any(f["rule_id"] == "TIME-002" for f in result["flags"])

def test_score_is_capped():
    result = analyze_resume(("Jan 2024 - Jan 2021\n" * 20) + "Improved system by 2000000 users")
    assert 0 <= result["risk_score"] <= 100

def test_no_llm_by_default():
    result = analyze_resume("Software engineer with Python experience.")
    assert result["engine"] == "Rules-based"
