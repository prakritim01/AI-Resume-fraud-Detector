# Viva addendum: Research extensions

**Why TF-IDF?** A lightweight, interpretable baseline. It weights terms by corpus frequency and uses cosine similarity; shared wording is easy to see. Its weakness is paraphrase sensitivity.

**Why Sentence-BERT?** It encodes sentences into vectors so semantic paraphrases can score closer. We compare it rather than assume it is better. It can still miss numeric contradictions and context.

**Why cosine similarity?** It measures vector orientation and is commonly used for similarity; it is scale-independent for normalized vectors. Scores are not probabilities.

**Why local Ollama?** It avoids sending resume text to an external API in this prototype and enables a repeatable local demonstration. It requires the model to be downloaded and running, and model outputs may vary.

**Why structured JSON output?** Makes fields easier to display, inspect, and test; reduces free-form output but does not guarantee factual accuracy.

**What is the benchmark?** Twenty synthetic paired examples labeled aligned/weak-support. It exercises code, but too small for statistically strong claims. A larger consented corpus, multiple annotators, agreement statistics, and category-wise error analysis are needed.

**What metrics?** Precision (fraction of flagged weak-support items that are weak-support), recall (fraction of weak-support examples detected), F1 (harmonic mean), accuracy, and confusion matrix. Threshold selection affects trade-offs. Report actual script outputs, not invented results.

**Does it detect fraud?** No. It identifies text-based review signals only. It cannot verify identities, employers, institutions, certificates, or truthfulness and must not decide hiring outcomes.
