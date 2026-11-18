# VeriResume — Explainable LLM-Assisted Resume Fraud Detector

A final-year B.Tech project prototype for **claim-level resume integrity review**. It extracts resume claims, checks timeline consistency, compares claims with candidate-supplied evidence, and produces an explainable review report. An optional local Ollama LLM provides advisory interpretation.

> **Ethical boundary:** VeriResume does not prove fraud, authenticate documents, estimate a real-world probability of dishonesty, or make hiring decisions. It surfaces review signals for a human reviewer. Missing evidence is not proof of fabrication.

## 1. Features

- Upload PDF, DOCX or TXT resumes, or paste text.
- Extract education, certifications, roles, date ranges, quantified achievements, contact details and links.
- Detect selected timeline anomalies, repeated statements and large quantified claims needing context.
- Compare extracted claims with optional evidence text using transparent lexical overlap.
- Optional local LLM advisory through Ollama; the app works without it.
- Explain every flag with rule ID, reason, points and suggested human verification.
- Export TXT and JSON reports.
- Unit tests for core extraction and scoring.

## 2. Setup (Windows PowerShell)

```powershell
# 1. Extract the ZIP and open this folder in VS Code
cd VeriResume_AI_Resume_Fraud_Detector

# 2. Create and activate virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Start the app
streamlit run app.py
```

The browser will open at `http://localhost:8501`. Rules-based analysis requires no API key and no internet connection after installation.

### Optional local LLM (Ollama)

1. Install Ollama from https://ollama.com.
2. In PowerShell, run:
   ```powershell
   ollama pull llama3.1:8b
   ollama serve
   ```
3. Keep Ollama running. In the app sidebar, select **Rules + optional Ollama**, check **Use Ollama if available**, and enter the model name you pulled.

The LLM is used only for advisory interpretation. Deterministic rules still produce the score. If Ollama is unavailable, the application falls back gracefully.

## 3. Run tests

```powershell
pytest -q
```

## 4. Demo quickly

Upload `sample_data/sample_resume.txt`. It intentionally contains a reversed date range so that you can demonstrate an explainable timeline flag. It is fictional test data, not a real person's resume.

## 5. System architecture

```text
PDF / DOCX / TXT / pasted text
              |
        Text extraction
              |
       Claim extraction
              |
     +--------+---------+
     |                  |
Timeline rules     Evidence matcher
     |                  |
     +--------+---------+
              |
      Transparent score
              |
  Optional local LLM advisory
              |
    Findings + human review
              |
       TXT / JSON report
```

## 6. Why these techniques?

| Component | Choice | Reason |
|---|---|---|
| Document parsing | pypdf, python-docx | Lightweight, local and easy to explain |
| Claim extraction | Regex + line-level heuristics | Deterministic baseline; inspectable; no training dataset needed |
| Timeline validation | Date parsing + chronological rules | Dates have explicit constraints; rules are reproducible |
| Evidence matching | Token overlap | Simple baseline that can be explained and tested; not treated as authentication |
| LLM | Optional Ollama local model | Adds semantic interpretation without requiring paid API access or sending resumes to a cloud service |
| Risk score | Weighted rule points, capped at 100 | Transparent prioritisation, not a misleading probability |
| UI | Streamlit | Fast way to build a usable research prototype and demo |

## 7. Important limitations / future work

This is a working academic prototype, not a production background-check product. Resume layouts vary; regex extraction can miss claims. Lexical overlap can miss paraphrases and can produce false matches. An LLM may hallucinate and must not be trusted as a verifier. No employer, university, or certificate issuer is contacted.

Strong future extensions:
1. Replace regex extraction with a labelled NER/LLM structured-output benchmark.
2. Add semantic retrieval (Sentence-BERT) for evidence-to-claim matching and compare it with lexical overlap.
3. Add document provenance / cryptographic hash tracking for uploaded evidence.
4. Integrate only authorised verification APIs or verified issuer records.
5. Evaluate precision, recall, F1 and false-positive rate on a consented, de-identified dataset.
6. Add reviewer feedback and threshold calibration.

## 8. Suggested evaluation plan

Create a small synthetic test set with categories: consistent timeline, reversed dates, overlapping full-time roles, unsupported certificate, metric needing context, and evidence wording paraphrase. Have two reviewers label whether each item requires review. Report precision, recall, F1 and false-positive rate for the review-flag task. Do not label people as fraudulent.

## 9. Project structure

```text
VeriResume_AI_Resume_Fraud_Detector/
├── app.py
├── requirements.txt
├── README.md
├── veriresume/
│   ├── __init__.py
│   ├── parser.py
│   ├── analyzer.py
│   └── report.py
├── sample_data/
│   └── sample_resume.txt
├── tests/
│   └── test_analyzer.py
└── docs/
    ├── PROJECT_REPORT_GUIDE.md
    └── VIVA_PREPARATION.md
```

---

# Research Extension Pack (2.0)

This extension adds an experiment suite for your Introduction to Large Language Models course:

- **LLM structured claim extraction**: local Ollama extracts claims into JSON fields, to compare with pattern-based extraction.
- **TF-IDF baseline**: word/phrase vectors and cosine similarity.
- **Sentence-BERT comparison**: optional `all-MiniLM-L6-v2` semantic embeddings.
- **Synthetic annotated benchmark**: 20 claim/evidence pairs with aligned / weak-support labels.
- **Benchmark script**: threshold sweeps for accuracy, precision, recall, and F1.
- **Local LLM reasoning**: Ollama structured JSON analysis with issue/gap/alternative/check fields.
- **Research paper draft, architecture flow, annotation guide, viva addendum**.

## Install research additions

Standard dependencies already include scikit-learn. For the optional Sentence-BERT experiment, install:

```powershell
pip install -r requirements-semantic.txt
```

The first Sentence-BERT run may download model weights and requires internet access. It can be skipped; TF-IDF still works.

## Run benchmark

```powershell
python research/benchmark.py
```

It prints metrics for threshold sweeps. **Do not treat these demo metrics as research findings**: the benchmark has only 20 synthetic examples. Use a larger consented, de-identified dataset and independent annotations before reporting performance claims.

## App research lab

After `streamlit run app.py`, scroll to **Research lab**:
1. Semantic comparison — paste a claim and evidence, compare TF-IDF and (if installed) Sentence-BERT cosine scores.
3. Annotated benchmark — browse/download the dataset and run the script.
4. LLM claim reasoning — call your local Ollama model for structured advisory output.

No cloud LLM/API calls are made. Resume text and evidence are handled locally by the app. Ollama must be installed and running for the LLM feature.

## Research honesty / safeguards
- The system does not authenticate documents or verify external entities.
- Similarity is textual alignment, not truth or fraud probability.
- LLM reasoning is advisory and can hallucinate.
- No automated hiring or candidate ranking decisions.
- The dataset is synthetic and small; results are demonstration only.

See `docs/RESEARCH_PAPER_DRAFT.md`, `docs/ARCHITECTURE.md`, `docs/DATASET_ANNOTATION_GUIDE.md`, and `docs/VIVA_RESEARCH_ADDENDUM.md` for report/viva material.
