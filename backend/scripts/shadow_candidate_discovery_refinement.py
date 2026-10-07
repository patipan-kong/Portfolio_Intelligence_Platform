"""Slice 1B replay-only reporting. No DB, market fetch or AI mode."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
from services.candidate_discovery_refinement import refine_capture  # noqa: E402


def render_report(result: dict) -> str:
    def percentage(value):
        return "UNKNOWN" if value is None else f"{value:.2f}%"

    baseline = result["baseline"]
    standalone = baseline["standalone"]
    lines = ["# Shadow Discovery — Slice 1B", "",
        "Offline structural comparison only. No default candidate set, production authority or investment advice.", "",
        "## Slice 1 baseline preserved", "",
        f"As of: {standalone['as_of']}; coverage: {standalone['coverage']}",
        f"Legacy labels: {baseline['legacy']['signal_distribution']}; L1 gate: {baseline['legacy']['l1_eligible_count']}.",
        f"Captured-input legacy top ten: {baseline['legacy']['captured_order_top_10']}.",
        "Exact current-runtime selection remains UNPROVEN. Original capture/result/report were not overwritten.", "",
        "## Slice 1B: exclusion diagnosis", "",
        "Eligibility unchanged. No sector-specific applicability rule is established by repository source.",
        "Supplemental raw cache is diagnostic only, not proven original baseline input and never used for ranking.", "",
        "| Symbol | Listing form | Baseline sector | Provider type / industry | Missing FA fields | Classification |",
        "|---|---|---|---|---|---|"]
    for row in result["exclusion_diagnosis"]:
        fields = ", ".join(f["field"] for f in row["fields"])
        classifications = "; ".join(f"{f['field']}: {f['classification']}" for f in row["fields"])
        lines.append(f"| {row['symbol']} | {row['listing_form']} | {row['baseline_sector']} | {row['provider_quote_type']} / "
            f"{row['provider_industry']} | {fields} | {classifications} |")
    lines.extend(["", "Field origins: PE = trailingPE or forwardPE; growth = revenueGrowth; ROE = returnOnEquity; "
        "debt/equity = debtToEquity. YahooProvider.get_fundamentals → fetch_info → analyze_fundamental → "
        "AgentCache → adapter. No sector-specific applicability flag is propagated.",
        "", "AIA06.BK → AIA and GOLDM01.BK → GLDM return ETF provider profiles. The existing stock/DR bindings "
        "and corporate FA coverage require review; no identity correction is made here.", "",
        "## Sector effects", "", f"Universe: {baseline['comparison']['universe_sector_distribution']}",
        f"Ranking eligible: {baseline['comparison']['ranking_eligible_sector_distribution']}", "",
        "## Temporal and provenance diagnosis", "", "```json"])
    temporal = {k: v for k, v in result["temporal"].items() if k != "candidates"}
    lines.extend([json.dumps(temporal, indent=2), "```", "",
        "Financial quarter/fiscal-year values in the supplement are provider reporting-period labels, "
        "not publication dates or observation dates for the baseline FA metrics.", "",
        "## Independent dimension leaders", ""])
    for name, group in result["dimension_leaders"].items():
        lines.extend([f"### {name}", "", f"Budget target {group['requested_budget']}; actual {group['actual_count']}; "
            f"boundary {group['boundary_value']}; ties preserved.", "",
            "| Symbol | Raw | Percentile | Sector | Held/new by portfolio |", "|---|---:|---:|---|---|"])
        for row in group["leaders"]:
            lines.append(f"| {row['symbol']} | {row['raw_score']} | {row['percentile']:.2f} | {row['sector']} "
                         f"| {row['held_new_by_portfolio']} |")
    lines.extend(["", f"Dimension coarseness: {result['dimension_coarseness']}",
        f"Joint dimension maxima: {result['joint_dimension_maxima']}. A security highest on both dimensions "
        "dominates every eligible security with a lower value on either dimension; Front 1 can legitimately collapse."])
    lines.extend(["", "## Pareto structure", "", "| Front | Count | Cumulative | Sectors |", "|---:|---:|---:|---|"])
    structure = result["pareto_structure"]
    for number, (size, cumulative, sectors) in enumerate(zip(structure["front_sizes"],
            structure["cumulative_counts"], structure["sector_composition_by_front"]), 1):
        lines.append(f"| {number} | {size} | {cumulative} | {sectors} |")
    lines.extend(["", f"Pair relationships: {structure['pair_relationships']}.", "",
        "## Candidate-set experiments", "",
        "Cumulative budget is a TOTAL target. Dimension-union budget is PER DIMENSION, with a nominal union bound "
        "of twice that budget before duplicate removal and explicit boundary-tie exceptions. These size targets differ.", "",
        "| Experiment | Actual | Overshoot | Membership |", "|---|---:|---:|---|"])
    for name, experiment in result["candidate_sets"].items():
        over = experiment.get("overshoot", experiment.get("above_nominal_bound", 0))
        lines.append(f"| {name} | {experiment['actual_count']} | {over} | {', '.join(experiment['symbols'])} |")
    lines.extend(["", "## Legacy comparisons", "",
        "Percentages show Discovery-set coverage / legacy-reference coverage. Complete difference lists are in result JSON.", "",
        "| Experiment | Reference | Overlap | Percentages | Legacy top-ten only / Discovery only |",
        "|---|---|---:|---|---|"])
    for name, experiment in result["candidate_sets"].items():
        for reference, comparison in experiment["legacy_comparison"].items():
            diff = (f"{comparison['legacy_only']} / {comparison['discovery_only']}"
                    if reference == "legacy_top_10" else "see structured result")
            lines.append(f"| {name} | {reference} | {comparison['overlap_count']} | "
                f"{percentage(comparison['percent_of_discovery_set'])} / {percentage(comparison['percent_of_legacy_set'])} | {diff} |")
        lines.append(f"\n{name} label distribution (diagnostic only): {experiment['label_distribution_diagnostic_only']}\n")
    lines.extend(["", "## Important cases", "",
        "| Symbol | Legacy label | FA | Timing | FA pct | Timing pct | Front | Legacy top ten | Missing/limited |",
        "|---|---|---:|---:|---:|---:|---:|---|---|"])
    for row in result["important_cases"]:
        if "status" in row:
            lines.append(f"| {row['symbol']} | {row['status']} | | | | | | | |")
            continue
        reason = ", ".join(row["ranking_eligibility"]["reasons"]) or "expired timing; mixed bar dates; FA epoch/version unknown"
        lines.append(f"| {row['symbol']} | {row['legacy_label']} | {row['fa']} | {row['timing']} | "
            f"{row['fa_percentile']} | {row['timing_percentile']} | {row['pareto_front']} | {row['legacy_top_10']} | {reason} |")
    names = list(result["candidate_sets"])
    lines.extend(["", "Candidate-set membership:", "",
                  "| Symbol | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)])
    for row in result["important_cases"]:
        if "membership" in row:
            lines.append("| " + row["symbol"] + " | " + " | ".join(
                "yes" if row["membership"][name] else "—" for name in names) + " |")
    lines.extend(["", "## Portfolio feasibility annotations", "",
        "Not blocked by known restrictions is not confirmed feasible. Current policy feasibility remains unknown.", "",
        "| Experiment | Portfolio | Held | New | Locked | Not blocked by known rules | Current feasible |",
        "|---|---|---:|---:|---|---:|---|"])
    for name, experiment in result["candidate_sets"].items():
        for portfolio in experiment["portfolio_diagnostics"]:
            lines.append(f"| {name} | {portfolio['portfolio_id']} | {len(portfolio['held'])} | {len(portfolio['new'])} "
                f"| {portfolio['locked']} | {portfolio['not_blocked_by_known_hard_restrictions_count']} | UNKNOWN |")
    for overlay in baseline["portfolio_overlays"]:
        lines.extend(["", f"Portfolio {overlay['portfolio_id']}: exposure source {overlay['exposure_source']}; "
            f"policy source {overlay['policy_source']}; captured sector weights {overlay['captured_sector_weights']}; "
            f"caps {overlay['captured_sector_caps']}. Historical annotations only."])
    lines.extend(["", "## Limits and decision questions", "",
        "Q1: Mixed/unresolved. Raw-provider missingness plus a stricter-than-producer universal complete-case rule; "
        "economic applicability is not established. Two ETF provider profiles introduce separate identity/profile concerns.",
        "", "Q2: Structural comparison only. Current-opportunity ranking and fully aligned point-in-time comparison are unsupported.",
        "", "Q3: Pareto exposes dominance, ties and incomparability without a weighted score; its investment usefulness is unproven.",
        "", "Q4: Front 1 alone is too narrow to provide a useful range of portfolio alternatives in this capture.",
        "", "Q5: Cumulative fronts broaden alternatives, but current feasibility and an appropriate budget remain unproven.",
        "", "Q6: FA + Timing suffices for another structural shadow iteration. Resolve identity, applicability and time alignment "
        "before adding another evidence dimension; no extra dimension is justified yet.",
        "", "Q7: Keep Discovery as the active research track; do not advance to Investor Intent Slice 2.", "",
        "SHADOW DISCOVERY INCONCLUSIVE — CONTINUE DISCOVERY RESEARCH"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--baseline-result", type=Path, required=True)
    parser.add_argument("--supplement", type=Path)
    parser.add_argument("--budgets", type=int, nargs="+", default=[5, 10, 15])
    parser.add_argument("--output-prefix", type=Path, required=True)
    args = parser.parse_args()
    outputs = [Path(f"{args.output_prefix}.result.json"), Path(f"{args.output_prefix}.md")]
    original_prefix = str(args.capture).removesuffix(".capture.json")
    protected = [args.capture, args.baseline_result, Path(f"{original_prefix}.md")]
    if args.supplement:
        protected.append(args.supplement)
    if {p.resolve() for p in outputs} & {p.resolve() for p in protected}:
        parser.error("output must not overwrite baseline or supplemental inputs")
    capture_bytes = args.capture.read_bytes()
    capture = json.loads(capture_bytes)
    saved = json.loads(args.baseline_result.read_text(encoding="utf-8"))
    supplement = json.loads(args.supplement.read_text(encoding="utf-8")) if args.supplement else None
    digest = hashlib.sha256(capture_bytes).hexdigest()
    if supplement and supplement["baseline_sha256"] != digest:
        parser.error("supplement must reference the same frozen capture")
    result = refine_capture(capture, supplement, tuple(args.budgets))
    if json.loads(json.dumps(result["baseline"])) != saved:
        parser.error("replayed baseline does not match the saved Slice 1 result")
    result["baseline_capture_sha256"] = digest
    result["baseline_result_sha256"] = hashlib.sha256(args.baseline_result.read_bytes()).hexdigest()
    outputs[0].parent.mkdir(parents=True, exist_ok=True)
    outputs[0].write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    outputs[1].write_text(render_report(result), encoding="utf-8")
    print(json.dumps({"eligibility": result["eligibility_refinement"], "temporal": {
        k: v for k, v in result["temporal"].items() if k not in ("candidates", "semantics")},
        "sets": {name: {k: v for k, v in exp.items() if k in ("actual_count", "included_fronts", "overshoot",
            "per_dimension_budget", "above_nominal_bound")} for name, exp in result["candidate_sets"].items()}}, indent=2))


if __name__ == "__main__":
    main()
