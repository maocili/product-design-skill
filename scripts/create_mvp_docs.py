#!/usr/bin/env python3
"""
Create deterministic MVP planning docs from a short idea input.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "output/product-plans"
MIN_BRIEF_IDEA_WORDS = 25

MOBILE_KEYWORDS = {
    "android",
    "app store",
    "camera",
    "ios",
    "location",
    "mobile",
    "notification",
    "offline",
    "on-the-go",
    "phone",
    "push",
    "smartphone",
    "touch",
}

WEB_KEYWORDS = {
    "admin",
    "analytics",
    "browser",
    "dashboard",
    "desktop",
    "portal",
    "saas",
    "website",
    "web",
}

BOTH_KEYWORDS = {
    "cross-platform",
    "cross platform",
    "multi-device",
    "multi device",
    "responsive",
    "omnichannel",
}


@dataclass
class PlatformDecision:
    recommended: str
    backup: str
    rationale: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate MVP planning docs from a short product idea."
    )
    parser.add_argument(
        "--idea",
        required=True,
        help="One-sentence or one-paragraph idea input.",
    )
    parser.add_argument(
        "--project",
        default="",
        help="Optional project name. If omitted, it is inferred from the idea.",
    )
    parser.add_argument(
        "--output-root",
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Output root folder. Defaults to {DEFAULT_OUTPUT_ROOT}.",
    )
    parser.add_argument(
        "--slug",
        default="",
        help="Optional folder slug. If omitted, derived from project name.",
    )
    parser.add_argument(
        "--date",
        default="",
        help="Optional date for output folder in YYYY-MM-DD format.",
    )
    return parser.parse_args()


def normalize_whitespace(text: str) -> str:
    return " ".join(text.strip().split())


def infer_project_name(idea: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", idea)
    if not words:
        return "Idea MVP"
    trimmed = words[:6]
    return " ".join(word.capitalize() for word in trimmed)


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "mvp-plan"


def parse_or_today_date(raw_date: str) -> str:
    if not raw_date:
        return date.today().isoformat()
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("--date must match YYYY-MM-DD.") from exc
    return raw_date


def find_hits(text: str, keywords: set[str]) -> list[str]:
    lowered = text.lower()
    hits = [word for word in keywords if word in lowered]
    return sorted(hits)


def infer_platform_decision(idea: str) -> PlatformDecision:
    mobile_hits = find_hits(idea, MOBILE_KEYWORDS)
    web_hits = find_hits(idea, WEB_KEYWORDS)
    both_hits = find_hits(idea, BOTH_KEYWORDS)

    if both_hits or (mobile_hits and web_hits):
        recommended = "Both"
        backup = "Web"
    elif mobile_hits and not web_hits:
        recommended = "Mobile"
        backup = "Web"
    else:
        recommended = "Web"
        backup = "Mobile"

    rationale_parts: list[str] = []
    if both_hits:
        rationale_parts.append(
            f"cross-device signals detected ({', '.join(both_hits)})"
        )
    if mobile_hits:
        rationale_parts.append(
            f"mobile signals detected ({', '.join(mobile_hits)})"
        )
    if web_hits:
        rationale_parts.append(f"web signals detected ({', '.join(web_hits)})")
    if not rationale_parts:
        rationale_parts.append(
            "no explicit platform signals detected, defaulting to Web for fastest MVP delivery"
        )

    rationale = "; ".join(rationale_parts)
    return PlatformDecision(recommended=recommended, backup=backup, rationale=rationale)


def build_assumptions(idea: str) -> list[str]:
    assumptions = [
        "Target user segment is inferred from the idea and needs stakeholder confirmation.",
        "The core user pain is prioritized over secondary workflows for MVP scope.",
    ]
    if len(idea.split()) < MIN_BRIEF_IDEA_WORDS:
        assumptions.append(
            "Input idea is brief, so feature boundaries and business constraints are provisional."
        )
    return assumptions


def build_summary_doc(
    *,
    project: str,
    idea: str,
    decision: PlatformDecision,
    assumptions: list[str],
    run_date: str,
) -> str:
    assumption_lines = "\n".join(f"- {item}" for item in assumptions)
    return f"""# MVP Summary: {project}

## Metadata
- Date: {run_date}
- Output language: English

## Idea Input
{idea}

## Problem Statement
Users need a faster and clearer way to achieve the intended outcome described in the idea, without relying on fragmented manual workarounds.

## Target User
- Primary segment: [Define specific user segment]
- Trigger moment: [Define when they need this solution]
- Current alternative: [Define what they use today]

## One-Line Unique Value Proposition
For [target user], **{project}** helps them [core job-to-be-done] by [unique mechanism], unlike [current alternative].

## Platform Recommendation
- Recommended platform: **{decision.recommended}**
- Backup platform: **{decision.backup}**
- Rationale: {decision.rationale}

## MVP Scope Boundary
### In Scope (Must)
- Deliver one end-to-end path for the primary user job.
- Capture the minimum data required to complete that path.
- Track the core success metric from day one.

### Out of Scope (Not in MVP)
- Advanced personalization.
- Deep integrations beyond one critical dependency.
- Non-essential automation and reporting.

## First Validation Action
- Smallest experiment: Ship a concierge or lightweight pilot for one high-priority user segment.
- Success signal: At least 5 target users complete the core flow and report clear value.
- Failure threshold: Fewer than 2 users complete the core flow or no repeat intent appears.
- Decision gate: Decide whether to iterate scope, pivot segment, or proceed to broader build.

## Assumptions
{assumption_lines}
"""


def build_detailed_doc(
    *,
    project: str,
    idea: str,
    decision: PlatformDecision,
    assumptions: list[str],
    run_date: str,
) -> str:
    assumption_lines = "\n".join(f"- {item}" for item in assumptions)
    return f"""# MVP Plan: {project}

## 1. Metadata
- Date: {run_date}
- Output language: English
- Planning mode: Documentation only (no clickable prototype by default)

## 2. Product Concept
### 2.1 Idea Input
{idea}

### 2.2 Concept Definition
- Product concept: [Describe the product in 2-3 sentences]
- Intended user outcome: [Describe measurable user outcome]
- Business outcome: [Describe measurable business objective]

## 3. Platform Decision
- Recommended platform: **{decision.recommended}**
- Backup platform: **{decision.backup}**
- Decision rationale: {decision.rationale}
- Revisit trigger: Re-evaluate platform after first validation cycle if completion and retention differ from expectation.

## 4. Value Proposition Canvas
### 4.1 Customer Profile
- Customer Jobs:
  - [Functional job]
  - [Emotional or social job]
- Pains:
  - [Current friction]
  - [Current risk or blocker]
- Gains:
  - [Desired improvement]
  - [Desired confidence or speed]

### 4.2 Value Map
- Products and Services:
  - [MVP product element]
  - [MVP service or support element]
- Pain Relievers:
  - [How the MVP removes friction]
  - [How the MVP reduces risk]
- Gain Creators:
  - [How the MVP creates measurable improvement]
  - [How the MVP increases confidence or control]

### 4.3 One-Line UVP
For [target user], **{project}** helps [core job] by [unique mechanism], unlike [current alternative].

## 5. MVP Scope and Prioritization Boundary
### Must
- One end-to-end flow for the primary user job.
- One onboarding approach that gets users to first value quickly.
- Instrumentation for core funnel and one outcome metric.

### Should
- One retention-oriented reminder or re-entry trigger.
- One lightweight admin or support view if needed for operations.

### Won't (This MVP)
- Broad role/permission systems.
- Secondary workflows with low validation value.
- Complex integrations that are not required to prove unique value.

## 6. Key User Flow Narrative
1. User recognizes a trigger moment and enters the product.
2. User provides the minimum required inputs.
3. Product returns the core value outcome quickly.
4. User confirms the result and chooses next action.
5. Product records success event and prompts repeat behavior.

## 7. Risks and Assumptions
### Key Risks
- Segment mismatch: chosen users may not experience the pain intensely enough.
- Scope inflation: non-critical features may dilute validation speed.
- Channel mismatch: acquisition channel may not deliver target users consistently.

### Assumptions
{assumption_lines}

## 8. Validation Plan and Metrics
### 8.1 Smallest Experiment
- Run a 1-2 week pilot with a narrow segment and constrained scope.

### 8.2 Success Signals
- At least 5 users complete the core flow.
- At least 60% of pilot users report clear usefulness.
- At least 30% of pilot users return for a second usage cycle.

### 8.3 Failure Threshold
- Fewer than 2 users complete the core flow, or less than 20% return for repeat usage.

### 8.4 Decision Gate
- If success signals pass: proceed to implementation hardening.
- If mixed signals: tighten segment and rerun experiment.
- If failure threshold is hit: revise concept or reposition the value proposition.

### 8.5 Core Metrics
- Activation: first successful completion rate.
- Time-to-value: median time from entry to first successful outcome.
- Repeat intent: percentage of users indicating they would reuse within one week.

## 9. Immediate Next Steps
1. Confirm target segment and pain statement with stakeholders.
2. Translate Must scope into implementation tickets.
3. Prepare pilot instrumentation and reporting.
4. Schedule decision review at the end of the validation cycle.
"""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()

    idea = normalize_whitespace(args.idea)
    if not idea:
        raise ValueError("--idea cannot be empty after normalization.")

    project = normalize_whitespace(args.project) if args.project else infer_project_name(idea)
    run_date = parse_or_today_date(args.date)
    slug = normalize_whitespace(args.slug) if args.slug else slugify(project)

    decision = infer_platform_decision(idea)
    assumptions = build_assumptions(idea)

    output_root = Path(args.output_root)
    output_dir = output_root / f"{run_date}-{slugify(slug)}"
    summary_path = output_dir / "00-summary.md"
    detail_path = output_dir / "01-mvp-plan.md"

    summary_content = build_summary_doc(
        project=project,
        idea=idea,
        decision=decision,
        assumptions=assumptions,
        run_date=run_date,
    )
    detailed_content = build_detailed_doc(
        project=project,
        idea=idea,
        decision=decision,
        assumptions=assumptions,
        run_date=run_date,
    )

    write_file(summary_path, summary_content)
    write_file(detail_path, detailed_content)

    print(f"[OK] Created {summary_path}")
    print(f"[OK] Created {detail_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
