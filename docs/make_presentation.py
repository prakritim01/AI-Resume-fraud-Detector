from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
r=Presentation(); r.slide_width= Inches(13.333); r.slide_height= Inches(7.5)
NAVY=RGBColor(15,31,57); TEAL=RGBColor(40,190,180); WHITE=RGBColor(245,248,252); MUTED=RGBColor(185,200,218)
def slide(title, bullets=None, subtitle=None):
 s=r.slides.add_slide(r.slide_layouts[6]); bg=s.background.fill; bg.solid(); bg.fore_color.rgb=NAVY
 # accent stripe
 sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(.18), Inches(7.5)); sh.fill.solid(); sh.fill.fore_color.rgb=TEAL; sh.line.fill.background()
 tx=s.shapes.add_textbox(Inches(.75), Inches(.5), Inches(12), Inches(.9)); p=tx.text_frame.paragraphs[0]; p.text=title; p.font.size=Pt(32); p.font.bold=True; p.font.color.rgb=WHITE
 if subtitle:
  box=s.shapes.add_textbox(Inches(.8), Inches(1.55), Inches(11.8), Inches(.65)); p=box.text_frame.paragraphs[0]; p.text=subtitle; p.font.size=Pt(17); p.font.color.rgb=TEAL
 if bullets:
  box=s.shapes.add_textbox(Inches(.95), Inches(2.1 if subtitle else 1.7), Inches(11.4), Inches(5.1)); tf=box.text_frame; tf.word_wrap=True
  for i,b in enumerate(bullets):
   p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.text=b; p.font.size=Pt(22); p.font.color.rgb=WHITE; p.space_after=Pt(16); p.level=0
 return s
slide("VeriResume",subtitle="Explainable LLM-assisted resume claim review",bullets=["Final-year B.Tech project · Introduction to Large Language Models","Claim-level review signals with transparent methods","Human-in-the-loop decision support — not fraud verdicts"])
slide("Problem & motivation",["Resume claims are varied: dates, roles, skills, credentials, achievements, metrics.","Text-only screening can miss contradictions or create opaque decisions.","Goal: help reviewers inspect claims and evidence while avoiding automated candidate decisions."])
slide("Objectives",["Extract claim-like information and detect internal consistency signals.","Compare claim/evidence text with lexical and semantic baselines.","Use local LLM output for structured advisory interpretation.","Build an inspectable demo dataset and reproducible metric sweep."])
slide("System pipeline",["Document input (PDF/DOCX/TXT) → local text extraction → claim extraction","Timeline rules → transparent review flags and score breakdown","Evidence matching: TF-IDF cosine + optional Sentence-BERT cosine","Optional local Ollama LLM → issues, gaps, alternatives, suggested checks","Dashboard, export, benchmark results → human review"])
slide("Methods: why these choices?",["Rules: explicit date constraints are deterministic and easy to explain.","TF-IDF: fast lexical baseline; useful for matching shared terms, weak for paraphrases.","Sentence-BERT: semantic vector comparison; optional model, tested against baseline rather than assumed superior.","Ollama LLM: structured JSON reasoning locally; output can hallucinate and is advisory only."])
slide("Evaluation",["20 synthetic claim/evidence pairs; labels: aligned / weak-support.","Threshold sweep reports accuracy, precision, recall, F1 for TF-IDF and optional SBERT.","Use actual benchmark script outputs; do not present synthetic scores as real-world performance.","Future: consented de-identified corpus, multiple annotators, agreement statistics, category-level error analysis."])
slide("Demo flow",["Upload sample resume or fake test PDF; inspect claims and review flags.","Open Research Lab → compare lexical and semantic similarities.","Run benchmark script: python research/benchmark.py.","Run optional LLM analysis after installing Ollama and pulling a model.","Export report and JSON; explain one flag and its verification step."])
slide("Limitations & responsible use",["Similarity is not authenticity. Missing evidence is not proof of dishonesty.","No external employer/university/certificate verification is performed.","Regex parsing can miss layouts; LLMs can hallucinate; synthetic set is tiny.","No automated hiring decisions, rankings, or protected-characteristic analysis."])
slide("Conclusion & next steps",["Prototype combines explainable rules, lexical and optional semantic matching, and structured local LLM reasoning.","Next: grow annotated dataset, measure inter-annotator agreement, analyze errors, and calibrate reviewer thresholds.","Replace this slide with your measured results, project institution, and supervisor details before submission."])
r.save('/mnt/data/VeriResume_Research_Extended/docs/VeriResume_Project_Presentation.pptx')
