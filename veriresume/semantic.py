"""Evidence-to-claim similarity baselines: TF-IDF cosine and optional Sentence-BERT."""
from typing import Dict

def compare_claim_evidence(claim: str, evidence: str) -> Dict:
    result = {"claim": claim, "evidence": evidence, "tfidf_cosine": None, "sentence_bert_cosine": None,
              "tfidf_status": "unavailable", "sentence_bert_status": "not_run", "notes": []}
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vec = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
        matrix = vec.fit_transform([claim, evidence])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0,0])
        result["tfidf_cosine"] = round(score, 4)
        result["tfidf_status"] = "computed"
    except Exception as exc:
        result["notes"].append(f"TF-IDF baseline unavailable: {exc}")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        emb = model.encode([claim, evidence], normalize_embeddings=True)
        score = float(emb[0] @ emb[1])
        result["sentence_bert_cosine"] = round(score, 4)
        result["sentence_bert_status"] = "computed"
    except ImportError:
        result["sentence_bert_status"] = "dependency_missing"
        result["notes"].append("Install optional sentence-transformers to run the semantic embedding baseline.")
    except Exception as exc:
        result["sentence_bert_status"] = "model_unavailable"
        result["notes"].append(f"Sentence-BERT did not run (model download/cache issue): {exc}")
    result["caution"] = "Similarity measures textual alignment only. It is not proof that evidence is genuine or that a claim is true."
    return result
