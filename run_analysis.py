from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
CRITERIA = [
    "specialization", "error_risk", "method_independence", "own_tools",
    "work_volume", "reuse", "parallelism", "own_memory",
    "independent_audit", "final_impact",
]


def tags(value: object) -> set[str]:
    return set(str(value).split(";")) if pd.notna(value) else set()


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def main() -> None:
    scores = pd.read_csv(ROOT / "data" / "candidate_scores.csv")
    scores["recomputed_total"] = scores[CRITERIA].sum(axis=1)
    if not (scores["recomputed_total"] == scores["total"]).all():
        raise ValueError("Stored totals do not match recomputed criterion totals")
    if (scores[CRITERIA].min().min() < 0) or (scores[CRITERIA].max().max() > 5):
        raise ValueError("Criterion scores must remain between 0 and 5")

    pair_rows: list[dict] = []
    for position, left in scores.iterrows():
        for _, right in scores.iloc[position + 1 :].iterrows():
            overlap = 100 * (
                0.50 * jaccard(tags(left.function_tags), tags(right.function_tags))
                + 0.15 * jaccard(tags(left.source_tags), tags(right.source_tags))
                + 0.15 * jaccard(tags(left.tool_tags), tags(right.tool_tags))
                + 0.20 * jaccard(tags(left.output_tags), tags(right.output_tags))
            )
            reviewer_ids = {"C06", "C33", "C34", "C35"}
            independence_conflict = (left.candidate_id in reviewer_ids) != (right.candidate_id in reviewer_ids)
            pair_rows.append({
                "left": left.candidate_id,
                "right": right.candidate_id,
                "left_name": left.candidate_name,
                "right_name": right.candidate_name,
                "overlap": round(overlap, 1),
                "independence_block": independence_conflict,
            })
    overlaps = pd.DataFrame(pair_rows).sort_values(["overlap", "left", "right"], ascending=[False, True, True])
    overlaps.head(50).to_csv(ROOT / "data" / "top_overlaps.csv", index=False)

    scenarios = pd.read_json(ROOT / "data" / "scenarios.json")
    scenarios.to_csv(ROOT / "data" / "scenario_counts.csv", index=False)
    product_matrix = json.loads((ROOT / "config" / "product_matrix.json").read_text(encoding="utf-8"))
    active = pd.DataFrame([{"product": key, "active_agents": len(value)} for key, value in product_matrix.items()])
    active.sort_values(["active_agents", "product"], ascending=[False, True]).to_csv(
        ROOT / "data" / "product_active_counts.csv", index=False
    )

    registry = json.loads((ROOT / "config" / "agent_registry.json").read_text(encoding="utf-8"))
    final_ids = [item["id"] for item in registry["agents"]]
    if len(final_ids) != 27 or len(final_ids) != len(set(final_ids)):
        raise ValueError("Recommended registry must contain 27 unique agents")

    summary = {
        "candidate_roles": int(len(scores)),
        "candidate_roles_above_threshold_38": int((scores.total >= 38).sum()),
        "pairwise_comparisons": int(len(overlaps)),
        "documented_fusions": 8,
        "recommended_agents": len(final_ids),
        "recommended_motors": 18,
        "recommended_bases": 10,
        "recommended_skills": 16,
        "recommended_gates": 13,
        "active_agents_min": int(active.active_agents.min()),
        "active_agents_max": int(active.active_agents.max()),
        "score_min": int(scores.total.min()),
        "score_median": float(scores.total.median()),
        "score_max": int(scores.total.max()),
        "limitations": [
            "workload, SLA and budget were not supplied",
            "candidate scores are expert judgments, not empirical performance measures",
            "PDF containers were sampled and inventoried, not validated work-by-work in full",
            "architecture remains draft pending synthetic pilots A-H and retrabalho measurement",
        ],
    }
    (ROOT / "data" / "analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
