# Project Report Guide

Use this as the structure for your own report. Add your institution's required cover page, supervisor details, screenshots, implementation evidence and actual test results.

## Abstract
VeriResume is an explainable resume-integrity review prototype that applies document parsing, heuristic claim extraction, timeline consistency rules, evidence-text matching and optional local large-language-model interpretation. Rather than classifying a candidate as fraudulent, it surfaces specific claims that warrant human verification. The system provides traceable rule IDs, reasons, review steps and downloadable reports.

## Problem statement
Resume screening involves claims about employment, education, skills, certifications and achievements. Manual review is time-consuming, while a simple keyword classifier cannot explain why a claim is suspicious. The project explores a transparent, human-in-the-loop approach to prioritising claims for further review.

## Objectives
1. Parse common resume file formats.
2. Extract selected structured claims.
3. Identify explainable timeline and content anomalies.
4. Compare claims with candidate-provided evidence.
5. Explore an LLM as an advisory semantic reasoning layer.
6. Present findings with reasons and limitations.

## Methodology
Describe the pipeline in README.md. Explain that deterministic rules form the reproducible baseline. The optional LLM does not authenticate facts or determine the score. Compare outputs with LLM disabled/enabled during the demo.

## Evaluation
Use synthetic, consented examples. Define a *review flag* as the target label, not “fraud”. Report precision = TP/(TP+FP), recall = TP/(TP+FN), F1 = 2PR/(P+R), and false-positive rate = FP/(FP+TN). Include a confusion matrix and discuss limitations. Do not report invented performance numbers; calculate them from your actual labelled test set.

## Results and discussion
Include screenshots of upload, findings, extracted claims, explainability and exported report. Discuss false positives, missed anomalies, parsing limitations and LLM variability.

## Conclusion
Summarise whether the prototype successfully extracts claims and surfaces review-worthy inconsistencies. Emphasise that final verification remains human-led.
