"""Optional local Ollama claim reasoning. Advisory, schema-constrained output."""
import json, urllib.request, urllib.error

def reason_about_claim(claim: str, context: str = "", model: str = "phi3:latest", host: str = "http://localhost:11434"):
    prompt = f'''You are an academic research assistant for resume claim review. Do not declare fraud or infer intent.
Analyze the claim using only provided text. Return JSON with keys: claim_summary, possible_consistency_issues (array), evidence_gaps (array), alternative_explanations (array), suggested_human_checks (array), confidence_in_text_analysis (low|medium|high). Clearly distinguish text observations from unverifiable facts.
CLAIM: {claim}\nCONTEXT/EVIDENCE: {context or "None supplied"}'''
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "format": "json"}).encode()
    req = urllib.request.Request(host.rstrip("/") + "/api/generate", data=payload, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = json.loads(response.read().decode()).get("response", "")
        parsed = json.loads(raw)
        parsed["advisory_warning"] = "LLM output can be inaccurate. This is text interpretation, not verification or a hiring recommendation."
        return parsed
    except Exception as exc:
        return {"error": str(exc), "advisory_warning": "Start Ollama and confirm the model is installed. Do not interpret this failure as a resume finding."}

def extract_claims_with_local_llm(resume_text: str, model: str = "phi3:latest", host: str = "http://localhost:11434"):
    """LLM-assisted structured claim extraction. Claims remain unverified text."""
    prompt = f'''Extract resume statements into a structured claim inventory. Return JSON only with top-level key claims (array). Each item fields: claim_type (employment|education|skill|certification|achievement|project|publication|other), claim_text, dates_or_duration, entities, numeric_details, source_quote. Preserve wording and numbers. Do not infer missing facts. If a field is unknown use empty string or empty array. Do not judge truth or fraud.\nRESUME TEXT:\n{resume_text[:16000]}'''
    payload=json.dumps({"model":model,"prompt":prompt,"stream":False,"format":"json"}).encode()
    req=urllib.request.Request(host.rstrip("/")+"/api/generate",data=payload,headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=180) as response:
            raw=json.loads(response.read().decode()).get("response","")
        data=json.loads(raw)
        if not isinstance(data.get("claims"),list): raise ValueError("JSON response did not contain claims list")
        data["warning"]="LLM extraction is approximate. Extracted claims are not verified facts. Review against source resume."
        return data
    except Exception as exc:
        return {"error":str(exc),"warning":"LLM unavailable or output invalid. Use existing rule-based extraction instead."}

