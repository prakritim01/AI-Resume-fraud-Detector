# Dataset annotation guide

## Labels
- `aligned`: excerpt text is consistent with the claim in key details, allowing reasonable paraphrase or rounding.
- `weak_support`: excerpt is missing key detail, contradicts an important detail, or only partially supports the claim.

## Annotation unit
One resume claim paired with one candidate-supplied evidence excerpt. Labels describe textual support, not authenticity or candidate intent.

## Guidelines
1. Preserve important numbers, units, dates, organizations, credentials and role scope.
2. Small rounding differences may be aligned if units and context match (e.g., 12% vs 11.7%).
3. Contradictory metrics, dates, credential types, durations, or ownership are weak-support.
4. Missing details do not prove fabrication; label weak-support as a text-evidence gap.
5. Ambiguous cases should be marked for adjudication in a future dataset extension.
6. Record annotator ID (pseudonym), rationale, and disagreement; do not store personal data.

The current 20-row sample is synthetic, illustrative, and not statistically representative.
