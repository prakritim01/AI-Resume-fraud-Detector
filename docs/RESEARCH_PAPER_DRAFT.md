# VeriResume: Explainable Resume Claim Review Using Lexical, Semantic and Local LLM Methods

**Student research draft — customize with your institution, authors, actual experiments, and measured results.**

## Abstract
Resume integrity review is difficult to automate responsibly because resumes contain heterogeneous claims, evidence may be incomplete, and text similarity does not establish authenticity. This project presents VeriResume, a decision-support prototype that extracts claim-like text, applies transparent timeline and consistency rules, compares claims with candidate-provided evidence using TF-IDF cosine similarity and an optional Sentence-BERT embedding baseline, and requests structured advisory reasoning from an optional local LLM. The system reports claim-level observations and suggested human checks rather than predicting fraud or making hiring decisions. A small synthetic annotated benchmark is included to exercise the evaluation pipeline. The benchmark is a software demonstration only; it is not sufficient for generalizable conclusions. Future evaluation should use consented, de-identified data, independent annotators, inter-annotator agreement, and error analysis.

## 1. Introduction
Resume screening systems can be opaque and can amplify unfairness when they produce definitive labels from incomplete data. VeriResume narrows its task to surfacing textual consistency signals for human review. The research question is: *How do lexical and semantic similarity baselines differ when comparing resume claims with supplied evidence, and how can an LLM provide structured explanations without becoming the decision-maker?*

## 2. Related technique background
- **Rule-based consistency checks:** explicit date/order constraints are easy to inspect and reproduce, but pattern coverage is limited.
- **TF-IDF:** weighted word and phrase representation; cosine similarity is a lexical baseline. It may under-score paraphrases and can over-score shared vocabulary.
- **Sentence-BERT:** sentence embeddings represent meaning in a vector space; cosine similarity may better capture paraphrases, but embeddings can be wrong, biased, or insensitive to important numbers.
- **LLM structured reasoning:** local model returns observations, evidence gaps, alternative explanations, and suggested checks in JSON. It may hallucinate and is not used to authenticate facts.

## 3. System design
Document text is parsed locally, claims are extracted with patterns/heuristics, timeline rules generate transparent review signals, and optional evidence is compared with TF-IDF and Sentence-BERT. The optional Ollama reasoning layer receives one claim and context and returns structured advisory fields. The UI separates heuristic flags from research similarity scores and LLM output.

## 4. Dataset
The shipped benchmark contains 20 synthetic claim/evidence pairs with two labels: `aligned` and `weak_support`. Examples include matching certifications, paraphrased achievements, metric discrepancies, unsupported skills, role ownership, and timeline duration mismatch. This data is deliberately synthetic and small; it is suitable for testing but not for claims about real resumes or hiring populations.

## 5. Evaluation methodology
Use claim/evidence similarity scores as continuous values. Sweep thresholds and calculate accuracy, precision, recall, and F1 for the benchmark's binary label. Report confusion matrices and inspect false positives/negatives. Do not pick a threshold based on a tiny dataset and present it as universal. For a stronger study: collect a consented and de-identified dataset; define annotation rules before labeling; use at least two annotators; report Cohen's kappa (or another justified agreement measure); separate train/dev/test if training; evaluate by claim category; and document dataset limitations.

## 6. Ethical safeguards
No protected attributes are analyzed. A score is not a fraud probability. Missing evidence is not evidence of fabrication. No automatic rejection, ranking, or hiring recommendation is produced. Verification should be job-relevant, consent-based, and performed by authorized people.

## 7. Limitations
Regex extraction misses atypical formats; similarity scores are not authentication; synthetic benchmark results are not representative; LLM responses may hallucinate; local models vary by version and prompt; and no employer, school, or issuer is contacted. Document parsing may fail on scans or complex layouts.

## 8. Conclusion
VeriResume demonstrates an explainable, multi-method claim review workflow and a reproducible baseline comparison. Academic claims should be based only on measured experiments actually run by the student. The next steps are dataset expansion, annotation quality control, error analysis, and user study/reviewer feedback.

## References to add/verify in final submission
1. Salton, G. and Buckley, C. (1988), Term-weighting approaches in automatic text retrieval — verify bibliographic details.
2. Reimers, N. and Gurevych, I. (2019), Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks — verify citation details.
3. Ollama documentation for local model serving — cite the exact version/date consulted.
4. scikit-learn documentation for TF-IDF and cosine similarity — cite the pages/version consulted.
