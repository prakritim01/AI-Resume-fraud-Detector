import streamlit as st
import json
import pandas as pd
from veriresume.parser import extract_text
from veriresume.analyzer import analyze_resume
from veriresume.report import build_report
from veriresume.semantic import compare_claim_evidence
from veriresume.llm_reasoning import reason_about_claim, extract_claims_with_local_llm

st.set_page_config(page_title="VeriResume | Resume Integrity Analyzer", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.main {background: #f6f7fb;}
.block-container {padding-top: 1.6rem; max-width: 1250px;}
.hero {padding: 1.35rem 1.6rem; border-radius: 18px; background: linear-gradient(115deg,#172554,#334155); color:white; margin-bottom:1rem;}
.hero h1 {color:white; margin:0;}
.hero p {color:#dbeafe; margin:.35rem 0 0 0;}
.metric-card {background:white; border:1px solid #e5e7eb; border-radius:14px; padding:16px;}
.small-muted {color:#64748b;font-size:.88rem;}
</style>
<div class="hero">
<h1>🛡️ VeriResume</h1>
<p>Explainable LLM-assisted resume integrity analysis · Claim-level evidence · Human-in-the-loop review</p>
</div>
""", unsafe_allow_html=True)

st.info("VeriResume is a decision-support prototype. It flags claims for review; it does not prove that a candidate committed fraud. Do not use its score as an automated hiring decision.")

with st.sidebar:
    st.header("Analysis settings")
    llm_mode = st.selectbox("Claim interpretation engine", ["Rules + optional Ollama", "Rules only"], help="Rules-only works without an API key or internet. Ollama can add local LLM explanations.")
    ollama_model = st.text_input("Ollama model", value="llama3.1:8b", disabled=(llm_mode != "Rules + optional Ollama"))
    use_ollama = st.checkbox("Use Ollama if available", value=False, disabled=(llm_mode != "Rules + optional Ollama"))
    st.caption("For local LLM mode, install Ollama and pull a model first. The app gracefully falls back to rules if unavailable.")
    st.divider()
    st.caption("Prototype version 1.0 · Academic project")

left, right = st.columns([1.05, .95], gap="large")
with left:
    st.subheader("1. Upload a resume")
    uploaded = st.file_uploader("Supported formats: PDF, DOCX, TXT", type=["pdf", "docx", "txt"])
    pasted = st.text_area("Or paste resume text", height=250, placeholder="Paste resume text here...")
    resume_text = ""
    if uploaded is not None:
        try:
            resume_text = extract_text(uploaded.getvalue(), uploaded.name)
            st.success(f"Extracted {len(resume_text.split())} words from {uploaded.name}")
        except Exception as e:
            st.error(f"Could not read this file: {e}")
    if pasted.strip():
        resume_text = pasted.strip()
    st.subheader("2. Add supporting evidence (optional)")
    evidence = st.text_area("Paste evidence supplied by the candidate", height=135,
        placeholder="Example: AWS certification ID ...; employment verification letter says ...")
    st.caption("Evidence is treated as user-provided context, not independently authenticated documentation.")

with right:
    st.subheader("What the system checks")
    st.markdown("""
    - **Claim extraction:** employers, roles, dates, education, certifications, skills and quantified achievements.
    - **Internal consistency:** date conflicts, future dates, impossible durations and mismatched timelines.
    - **Evidence alignment:** whether supplied evidence appears to support a claim.
    - **Risk explanation:** transparent rule contributions and LLM-generated interpretation when enabled.
    - **Human review:** every flag includes a reason and a suggested next verification step.
    """)
    st.warning("A high score means more review signals were found. It is not a probability that the resume is fraudulent.")

run = st.button("🔍 Analyze resume", type="primary", disabled=not bool(resume_text.strip()), use_container_width=True)
if run:
    with st.spinner("Extracting claims and evaluating consistency..."):
        result = analyze_resume(resume_text, evidence=evidence, use_ollama=use_ollama,
                                ollama_model=ollama_model)
    st.session_state["analysis_result"] = result
    st.session_state["resume_text"] = resume_text

if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    st.divider()
    st.subheader("Analysis overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Review risk score", f'{result["risk_score"]}/100')
    c2.metric("Claims extracted", result["claim_count"])
    c3.metric("Review flags", len(result["flags"]))
    c4.metric("Analysis engine", result["engine"])
    st.progress(result["risk_score"] / 100)
    st.caption(result["risk_band"] + " · Score is a prioritisation aid, not a fraud probability.")

    tabs = st.tabs(["🚩 Findings", "🧾 Extracted claims", "🧠 Method & explainability", "📄 Export report"])
    with tabs[0]:
        if not result["flags"]:
            st.success("No rule-based review flags were identified. This does not independently verify the claims.")
        for i, flag in enumerate(result["flags"], 1):
            with st.expander(f'{i}. [{flag["severity"]}] {flag["title"]}', expanded=(i <= 3)):
                st.write(flag["description"])
                st.markdown(f'**Related claim:** {flag.get("claim", "Resume-level pattern")}')
                st.markdown(f'**Why it was flagged:** {flag["reason"]}')
                st.markdown(f'**Suggested human verification:** {flag["next_step"]}')
                st.caption(f'Rule ID: {flag["rule_id"]} · Points: {flag["points"]}')
    with tabs[1]:
        claims = result["claims"]
        if claims:
            df = pd.DataFrame(claims)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.write("No structured claims were extracted. Try a text-based PDF or paste the resume text.")
    with tabs[2]:
        st.markdown("**Pipeline**")
        st.code("Resume → Text extraction → Claim extraction → Consistency rules → Evidence matching → Risk aggregation → Human review", language="text")
        st.markdown("**Scoring design**")
        st.write("Each independent review signal contributes a capped number of points. The total is capped at 100. This is a transparent heuristic score, not a trained probability model.")
        st.json(result["score_breakdown"])
        if result.get("llm_notes"):
            st.markdown("**LLM interpretation (advisory only)**")
            st.write(result["llm_notes"])
        st.markdown("**Limitations**")
        st.write("The prototype cannot authenticate employers, contact universities, validate certificate issuers, or reliably infer intent. Dates and entity extraction use lightweight patterns and may miss unusual resume layouts.")
    with tabs[3]:
        report = build_report(result)
        st.download_button("⬇️ Download analysis report (.txt)", report, file_name="veriresume_report.txt", mime="text/plain")
        st.download_button("⬇️ Download findings (.json)", json.dumps(result, indent=2), file_name="veriresume_findings.json", mime="application/json")

st.divider()
st.markdown('<p class="small-muted">Built for academic demonstration. Use consent-based, job-relevant evidence only. Avoid protected characteristics and do not make hiring decisions from this prototype.</p>', unsafe_allow_html=True)


# Research / evaluation suite: separate from the heuristic review score.
st.divider()
st.header("🔬 Research lab: semantic evidence & LLM experiments")
st.caption("These experiments are separate from the review score and are intended for academic comparison.")
research_tabs = st.tabs(["Transformer claim extraction", "Semantic comparison", "Annotated benchmark", "LLM claim reasoning"])
with research_tabs[0]:
    st.markdown("**Extract structured claims using a local LLM (transformer-based model served by Ollama).** This is compared conceptually with the rule/pattern extractor in the main analysis.")
    extraction_text=st.text_area("Resume text for semantic claim extraction", key="llm_extraction_text", height=160, placeholder="Paste resume text here, or copy text from the uploaded resume above")
    extraction_model=st.text_input("Ollama model for extraction", value="llama3.1:8b", key="extraction_model")
    if st.button("Extract claims with local LLM", key="extract_llm_claims", disabled=not extraction_text.strip()):
        with st.spinner("LLM is extracting structured claims..."):
            st.session_state["llm_extraction_result"]=extract_claims_with_local_llm(extraction_text,extraction_model)
    if st.session_state.get("llm_extraction_result"):
        st.json(st.session_state["llm_extraction_result"])
        st.caption("Review these outputs against the source document. This is extraction, not verification.")
with research_tabs[1]:
    st.markdown("**Compare TF-IDF lexical similarity against optional Sentence-BERT semantic similarity.**")
    claim_input = st.text_area("Claim to compare", key="semantic_claim", placeholder="e.g., Reduced API latency by 30% through caching")
    evidence_input = st.text_area("Evidence excerpt", key="semantic_evidence", placeholder="e.g., Added caching; endpoint response time improved by thirty percent")
    if st.button("Compare similarity", key="semantic_run", disabled=not (claim_input.strip() and evidence_input.strip())):
        with st.spinner("Computing lexical and (if installed) semantic similarity..."):
            comparison = compare_claim_evidence(claim_input, evidence_input)
        st.session_state["semantic_result"] = comparison
    if st.session_state.get("semantic_result"):
        comp=st.session_state["semantic_result"]
        a,b=st.columns(2)
        a.metric("TF-IDF cosine", comp.get("tfidf_cosine") if comp.get("tfidf_cosine") is not None else "Unavailable")
        b.metric("Sentence-BERT cosine", comp.get("sentence_bert_cosine") if comp.get("sentence_bert_cosine") is not None else "Not run")
        st.json(comp)
        st.warning(comp.get("caution", "Similarity is not verification."))
        if comp.get("notes"): st.info("\n".join(comp["notes"]))
with research_tabs[2]:
    st.markdown("The project ships a **20-row synthetic, annotated claim/evidence set** with aligned vs weak-support labels. Run benchmark script to reproduce threshold metrics.")
    st.code("python research/benchmark.py", language="powershell")
    try:
        bench=pd.read_csv("research/annotated_claim_evidence.csv")
        st.dataframe(bench, use_container_width=True, hide_index=True)
        st.download_button("Download benchmark CSV", bench.to_csv(index=False), "annotated_claim_evidence.csv", "text/csv")
    except Exception as e: st.error(f"Benchmark CSV unavailable: {e}")
    st.info("Dataset is synthetic and small. Use it to test code and methodology, not to claim real-world performance. Expand it with consented, de-identified annotations and agreement analysis for a research-grade evaluation.")
with research_tabs[3]:
    st.markdown("**Optional local LLM: claim-level structured reasoning with Ollama.** The model proposes issues, gaps, alternate explanations and human checks; it never labels a person fraudulent.")
    llm_claim=st.text_area("Claim for advisory reasoning", key="llm_claim", placeholder="Paste one resume claim")
    llm_context=st.text_area("Supporting context/evidence", key="llm_context", placeholder="Paste related evidence excerpt (optional)")
    llm_name=st.text_input("Local Ollama model", value="llama3.1:8b", key="research_llm_model")
    if st.button("Run local LLM reasoning", key="llm_reason", disabled=not llm_claim.strip()):
        with st.spinner("Calling local Ollama model..."):
            st.session_state["llm_reason_result"]=reason_about_claim(llm_claim,llm_context,llm_name)
    if st.session_state.get("llm_reason_result"): st.json(st.session_state["llm_reason_result"])
    st.caption("Ollama must be installed, running, and have the selected model pulled. LLM output is advisory and can be incorrect.")
