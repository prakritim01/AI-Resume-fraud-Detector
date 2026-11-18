"""Evaluate similarity baselines on the included small, synthetic annotated set.
Run from project root: python research/benchmark.py
"""
import csv, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

PATH=os.path.join(os.path.dirname(__file__),"annotated_claim_evidence.csv")
with open(PATH,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
texts=[r["claim"]+" "+r["evidence"] for r in rows]
# TF-IDF pairwise score, pairwise corpus vectorization. Similarity is a heuristic baseline.
vec=TfidfVectorizer(ngram_range=(1,2),stop_words="english")
X=vec.fit_transform([r["claim"] for r in rows]+[r["evidence"] for r in rows])
scores=[float(cosine_similarity(X[i],X[i+len(rows)])[0,0]) for i in range(len(rows))]
labels=[1 if r["label"]=="aligned" else 0 for r in rows]
print("Dataset size:",len(rows),"; positive/aligned:",sum(labels),"; weak-support:",len(labels)-sum(labels))
print("TF-IDF cosine threshold sweep (positive=aligned, negative=weak support)")
for threshold in [0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50]:
    pred=[1 if s>=threshold else 0 for s in scores]
    print(f"threshold={threshold:.2f} accuracy={accuracy_score(labels,pred):.3f} precision={precision_score(labels,pred,zero_division=0):.3f} recall={recall_score(labels,pred,zero_division=0):.3f} f1={f1_score(labels,pred,zero_division=0):.3f}")
try:
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    a=model.encode([r["claim"] for r in rows],normalize_embeddings=True)
    b=model.encode([r["evidence"] for r in rows],normalize_embeddings=True)
    sb_scores=[float(a[i]@b[i]) for i in range(len(rows))]
    print("\nSentence-BERT cosine threshold sweep")
    for threshold in [0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70]:
        pred=[1 if s>=threshold else 0 for s in sb_scores]
        print(f"threshold={threshold:.2f} accuracy={accuracy_score(labels,pred):.3f} precision={precision_score(labels,pred,zero_division=0):.3f} recall={recall_score(labels,pred,zero_division=0):.3f} f1={f1_score(labels,pred,zero_division=0):.3f}")
except Exception as e:
    print("Sentence-BERT skipped:",e,"\nInstall optional dependency and ensure model download/cache is available.")
print("\nCAUTION: tiny synthetic dataset; metrics are demonstration-only, not generalizable evidence.")
