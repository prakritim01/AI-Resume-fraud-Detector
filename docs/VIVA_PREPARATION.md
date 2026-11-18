# Viva Preparation — VeriResume

## 30-second explanation
“My project, VeriResume, is an explainable LLM-assisted resume integrity review system. It extracts claims from a resume, checks selected timeline inconsistencies, compares claims with supporting evidence text and produces a transparent review score with explanations. An optional local LLM helps interpret ambiguous claims, but it does not decide whether someone committed fraud. The goal is to support a human reviewer, not replace one.”

## Likely questions and clear answers

**1. Why did you choose this topic?**  
Resume screening is an important real-world NLP problem. A system that only says “fake” or “genuine” is difficult to trust. I focused on claim-level explanations and human review.

**2. Why is this an LLM project?**  
The project explores LLMs for interpreting natural-language claims and explaining ambiguity. The LLM can reason over extracted claims and user-supplied evidence text. It is optional so the baseline remains reproducible and usable without a paid API. Be honest: the current implementation's core extraction and score are rule-based, while the LLM is an advisory extension.

**3. Why not use only an LLM?**  
LLMs can hallucinate, vary between runs and be prompt-injected by document content. Deterministic rules are more reproducible for explicit constraints such as date ordering. A hybrid design uses rules for objective checks and an LLM only for semantic assistance.

**4. Why regex for claim extraction?**  
It provides a lightweight baseline that is easy to inspect and test. It is not sufficient for production. A next version could use spaCy NER or constrained LLM JSON extraction and compare precision/recall against this baseline.

**5. Why Ollama?**  
It runs a model locally, avoids a required paid API key and keeps resume text on the local machine. It also makes the LLM component demonstrable. Model quality and hardware requirements depend on the chosen model.

**6. How is fraud detected?**  
The app does not establish fraud. It identifies review signals such as reversed dates, future dates, duplicate statements and claims that need contextual evidence. Each flag has a reason and a suggested verification step.

**7. What does the risk score mean?**  
It is a weighted sum of configured rule points capped at 100. It is not a probability, confidence score or calibrated fraud likelihood. The weights are design choices that need evaluation and calibration on a labelled dataset.

**8. What is the evidence matcher doing?**  
It compares important tokens from extracted claims with tokens in evidence text. It is a baseline lexical retrieval method. It cannot authenticate a document and may miss paraphrases.

**9. How would you evaluate it?**  
Build a labelled dataset where the label means “needs human review”. Measure precision, recall, F1 and false-positive rate. Use a held-out test set and report the number and source of examples. Do not claim accuracy without measured results.

**10. What are the ethical risks?**  
False positives can unfairly harm candidates. Resume data is personal. The tool must use consent-based, job-relevant information, avoid protected traits, limit data retention and keep a human reviewer responsible for decisions.

**11. What is prompt injection and how do you address it?**  
A resume could contain text instructing the model to ignore prior instructions. The prompt explicitly treats resume/evidence as untrusted data, and the LLM is advisory only. A stronger implementation would isolate document content, validate structured outputs and test adversarial prompts.

**12. What is the main future improvement?**  
Use a labelled dataset and compare regex extraction with a domain-tuned NER model or structured-output LLM. Add semantic evidence retrieval and authorised external verification sources.

## Demo sequence
1. Start with `streamlit run app.py`.
2. Upload `sample_data/sample_resume.txt`.
3. Explain the reversed date range and future-year check.
4. Show extracted claims.
5. Add evidence text and rerun to show evidence matching.
6. Enable Ollama only if it is installed and running.
7. Download the report and explain the limitations.
