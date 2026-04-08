# Platform Decision Rules

Use these rules to recommend `Web`, `Mobile`, or `Both` from an idea input.

## 1. Decision Signals

### Strong Mobile Signals
- Idea explicitly mentions mobile app, iOS, Android, smartphone, push notifications, camera, or location-native behavior.
- Core value depends on in-the-moment or on-the-go interaction.

### Strong Web Signals
- Idea explicitly mentions dashboard, admin panel, browser workflow, portal, SaaS, or desktop-heavy tasks.
- Core value depends on dense data entry, analysis, or multi-pane views.

### Both Signals
- Idea explicitly calls for cross-device continuity, responsive experience, or multi-device usage.
- Both mobile and web signals appear with meaningful weight.

## 2. Recommendation Logic
- Recommend `Both` when cross-device intent is explicit or both signal sets are strong.
- Recommend `Mobile` when mobile signals dominate and web signals are weak.
- Recommend `Web` when web signals dominate or signals are ambiguous.
- Always include one backup recommendation.

## 3. Output Requirement
Always produce:
- Recommended platform
- Backup platform
- Explicit rationale with observed signals
- Revisit trigger (when to reassess the platform decision)

## 4. Practical Default
When signals are unclear, default to `Web` for fastest MVP delivery and lower distribution overhead.
