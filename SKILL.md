---
name: product-design-planning
description: Transform a one-sentence or one-paragraph product idea into execution-ready MVP planning documents. Use when requests ask to turn an idea into an MVP concept, define unique value with Value Proposition Canvas, recommend Web or Mobile or Both with rationale, set MVP scope boundaries, and design a first validation cycle.
---

# Product Design Planning

## Overview

Turn sparse idea input into documentation-first MVP plans that are ready for team alignment and first-round validation.
Default output language is English.

## Workflow

1. Decompose the idea.
- Capture target user, context, pain, trigger moment, and current alternatives.
- Infer only minimal assumptions and keep them explicit.

2. Decide platform strategy.
- Recommend one of `Web`, `Mobile`, or `Both`.
- State a backup option and explicit rationale.
- Follow [references/decision-rules-platform.md](references/decision-rules-platform.md).

3. Define unique value with VPC.
- Complete all Value Proposition Canvas blocks:
  - Customer Jobs
  - Pains
  - Gains
  - Products and Services
  - Pain Relievers
  - Gain Creators
- Derive one one-line UVP from the VPC.
- Follow [references/value-proposition-canvas-guide.md](references/value-proposition-canvas-guide.md).

4. Define MVP concept and boundaries.
- Describe concept, key user flow, and core assumptions.
- Set prioritization boundary with `Must`, `Should`, and `Won't`.
- Follow [references/mvp-concept-template.md](references/mvp-concept-template.md).

5. Generate dual-output documentation.
- Produce:
  - `00-summary.md` for fast alignment.
  - `01-mvp-plan.md` for execution details.
- Keep outputs in `output/product-plans/<YYYY-MM-DD>-<slug>/` by default.

6. Design first validation cycle.
- Define smallest useful experiment.
- Define success signals and failure threshold.
- Define decision gate and next action.
- Follow [references/validation-checklist.md](references/validation-checklist.md).

## Output Contract

### `00-summary.md`

- Include:
  - Problem statement
  - Target user
  - One-line UVP
  - Platform recommendation plus backup plus rationale
  - MVP scope boundary
  - First validation action
  - Assumptions

### `01-mvp-plan.md`

- Include:
  - Full VPC
  - Product concept definition
  - Key user flow narrative
  - Prioritization boundary
  - Risks and assumptions
  - Validation plan and metrics
  - Decision gate for next iteration

## Defaults

- Default language: English.
- Default mode: Documentation only, no clickable or high-fidelity prototype unless explicitly requested.
- Default output root: `output/product-plans`.
- Default behavior for missing details: Infer minimally and list assumptions explicitly.

## Deterministic Generator

Use the bundled script for deterministic scaffolding:

```bash
python3 scripts/create_mvp_docs.py --idea "Your idea sentence"
```

Optional flags:
- `--project`
- `--output-root` (default: `output/product-plans`)
- `--slug`
- `--date` in `YYYY-MM-DD`

The script writes:
- `00-summary.md`
- `01-mvp-plan.md`

## Resources

- `scripts/create_mvp_docs.py`: Deterministic doc generator.
- `references/mvp-concept-template.md`: Concept and scope template.
- `references/value-proposition-canvas-guide.md`: VPC guidance and quality checks.
- `references/decision-rules-platform.md`: Platform recommendation rules.
- `references/validation-checklist.md`: Validation cycle checklist.
- `assets/plan-pack-template/`: Optional markdown templates for manual editing.
