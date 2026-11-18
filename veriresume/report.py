def build_report(result):
    lines = [
        "VERIRESUME — RESUME INTEGRITY REVIEW",
        "=" * 48,
        f'Review score: {result["risk_score"]}/100',
        f'Priority band: {result["risk_band"]}',
        f'Claims extracted: {result["claim_count"]}',
        f'Engine: {result["engine"]}',
        "",
        "IMPORTANT: This score is not a probability of fraud. Flags are prompts for human review.",
        "",
        "FINDINGS",
        "-" * 48
    ]
    if not result["flags"]:
        lines.append("No rule-based flags were generated.")
    for i, f in enumerate(result["flags"], 1):
        lines += [f'{i}. [{f["severity"]}] {f["title"]} ({f["rule_id"]})',
                  f'   Claim: {f.get("claim", "")}',
                  f'   Reason: {f["reason"]}',
                  f'   Next step: {f["next_step"]}', ""]
    lines += ["EXTRACTED CLAIMS", "-" * 48]
    for c in result["claims"]:
        lines.append(f'- [{c["type"]}] {c["value"]}')
    if result.get("llm_notes"):
        lines += ["", "LLM ADVISORY NOTES", "-" * 48, result["llm_notes"]]
    lines += ["", "LIMITATIONS", "-" * 48,
              "This prototype cannot independently authenticate employers, institutions, or certificates.",
              "A missing match is not proof of fabrication. A human reviewer must inspect original evidence.",
              "Use only consent-based, job-relevant information and avoid protected characteristics."]
    return "\n".join(lines)
