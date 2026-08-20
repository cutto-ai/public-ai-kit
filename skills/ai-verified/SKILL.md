---
name: ai-verified
description: Run evidence-backed acceptance verification for interactive products from an approved case suite, record pass/fail/needs-decision results, file deduplicated defects when authorized, and feed escaped defects back into regression cases. Use when asked to verify a feature, execute acceptance cases, rerun regression, or turn a bug into a reusable verification case. Do not use for open-ended design critique, product ideation, or code-only unit-test authoring.
---

# AI Verified

Verify that an implemented product matches an approved specification. Keep four things separate:

- the **Skill** defines how verification is performed;
- a **case** is one approved assertion;
- a **suite** is the flat set of cases for one feature or workflow;
- a **run** records what happened against one build and environment.

The goal is not to judge whether the product decision is good. The goal is to determine whether observable behavior matches an approved expectation and to leave evidence another person can independently check.

## Inputs and authority

Before running, identify:

1. the suite or feature scope;
2. the target build and environment;
3. the approved source for each assertion;
4. the suite owner who can resolve ambiguity;
5. whether the user has authorized writes to an issue tracker or other external system.

Use an existing suite when available. Otherwise draft one from [the case-suite template](references/case-suite-template.md). Drafting does not make an assertion approved: the owner of the source requirement must approve it before a failure can be filed from it. Turn unresolved points into short forced-choice questions, and mark those cases `needs-decision` until answered.

Do not infer authority to test production, mutate real customer data, create tracker issues, assign people, change cycles or milestones, or alter issue status. A request to verify permits the interactions needed in the named test scope; external writes still require explicit or established workflow authorization.

## Preflight

Stop the run before producing product conclusions when any required channel is unavailable:

- the target cannot be reached or authenticated;
- required test data is missing or unsafe to modify;
- the browser or device cannot perform real interactions;
- screenshots, recordings, logs, or exported artifacts cannot be retained as evidence;
- the approved assertion or its owner cannot be identified.

Report these as environment or scope blockers, not product defects. Record which cases were not run.

If tracker writes are authorized, list existing open defects in scope before testing so the run can update a matching issue instead of creating a duplicate.

## Execute the suite

Run every `active` case and record exactly one result:

- `pass`: the approved assertion is met;
- `fail`: the observable result contradicts an approved assertion;
- `needs-decision`: the evidence is real, but the expected behavior is absent, ambiguous, outdated, or owned by someone else;
- `blocked`: the case could not be executed because its environment, data, or tool dependency failed.

Use four verification lenses across the suite:

| Lens | Inspect |
| --- | --- |
| Product and interaction | Critical path, feedback, loading, empty and error states, copy, keyboard and pointer behavior |
| Logic and state | Ordering, cross-view consistency, state transitions, persistence, undo/reset behavior, boundary combinations |
| Rendering | Truncation, overlap, placeholder leakage, stale selection or hover state, responsive layouts, accessibility-visible states |
| Data integrity | UI values against an authorized source of truth, degraded rendering for missing fields, import/export consistency |

### Interaction rules

- Use real pointer, keyboard, touch, or device input for every conclusion. Synthetic DOM events may help locate elements, but cannot prove a pass or failure.
- Judge user-visible output and computed visible style. Do not use private component flags, framework internals, or test-only attributes as the assertion unless the suite explicitly tests a developer contract.
- Do not guess that one control owns another element. Require a source-backed relationship.
- A missing feature is `needs-decision` unless the case explicitly says absence is a failure or the absence blocks the critical path.
- When the implementation and specification disagree, record the conflict and ask which source is current. Do not redesign the product during verification.
- Restore changed controls and test data to their starting state unless the suite defines a different cleanup contract.
- For toggles and options, test both enabled and disabled states. For exports, compare the actual artifact across states rather than trusting a success toast or filename.

For data-consistency cases, compare the interface with the most authoritative source available in the authorized scope: a test fixture, API response, stored record, or exported artifact. Interface self-consistency alone cannot prove correctness.

## Evidence contract

A `fail` requires evidence that shows the problem itself. Text-only claims are incomplete.

- Capture the smallest useful region while preserving enough context to identify the screen and state.
- Annotate the exact mismatch; use a short recording plus a still image when motion or timing exposes the failure.
- For comparisons, stack states vertically when that keeps text legible. Do not shrink full-screen images into unreadable collages.
- Record case ID, build, environment, viewport or device, timestamp, and the source assertion.
- Re-read captured evidence against the live state before filing it. Stale frames and wrong tabs are not evidence.
- Redact credentials, private endpoints, personal data, customer content, and unrelated browser chrome before uploading.

The optional `scripts/annotate-evidence.py` helper crops, enlarges, boxes, and stacks screenshots. It requires Pillow and operates only on local files.

Minimum evidence:

| Failure type | Minimum |
| --- | --- |
| Single visible state | One focused annotated image |
| Cross-view or cross-state mismatch | One legible labeled comparison |
| Interaction or timing failure | Short recording plus one annotated still |
| Export or data mismatch | Relevant UI evidence plus the compared artifact values or diff |

## Severity

Assign severity from user impact, not implementation effort:

| Level | Meaning |
| --- | --- |
| P0 | Critical path blocked, crash, security exposure, data loss, or incorrect write |
| P1 | Core behavior is wrong, essential functionality is partially unavailable, or visible data can mislead the user |
| P2 | State or feedback is wrong but a reasonable workaround exists; experience is degraded without misleading data |
| P3 | Non-blocking polish or minor consistency problem with limited user impact |

When uncertain between P1 and P2, ask whether the defect can make a user trust false information or take the wrong action. If yes, use P1; otherwise use P2.

## File or update defects

Only write to an issue tracker when authorized. Otherwise produce a ready-to-paste defect draft and keep the run log local.

Before creating an issue, search the scoped parent or project for the same user-visible symptom. Update an existing open issue with fresh evidence when it matches. Do not close, assign, schedule, or reprioritize issues unless the workflow explicitly grants that authority.

Use this defect structure:

1. target link or build identifier;
2. one-sentence problem statement with case ID and discovery time;
3. no more than four reproduction steps;
4. expected result tied to the approved assertion;
5. actual user-visible result with evidence embedded beside the claim;
6. user and workflow impact;
7. diagnostic direction written as a hypothesis, not a verdict;
8. environment details and the related case ID.

Quote interface text exactly. Prefer plain user-visible language over internal implementation terms. After writing, read the issue back and confirm the body, evidence, labels, parent link, and priority were actually saved.

Treat rejected approvals, rate limits, and connector failures as external-write blockers. Do not retry indefinitely or reinterpret them as product failures.

## Maintain the case system

Keep one human-readable suite file per feature or workflow. Cases stay flat in one table so the owner can review the whole acceptance contract at once. Start a new suite when the topic sentence changes.

Each case needs a stable ID, status, checkpoint, approved assertion and source, procedure, and expected severity. Retire cases instead of deleting them after they have appeared in a run or issue.

Every newly discovered defect must answer: **which case should have caught this?**

- If an existing case should have caught it, tighten that case's assertion, procedure, data, or evidence requirement and record the escaped-defect review.
- If no case covers it, draft a new case from the defect's approved expected result, record the defect as its origin, and obtain owner approval before activating it.

Append every execution to the suite run log. Do not rewrite prior runs.

## Regression mode

For regression, select the smallest suite set affected by the change; reserve all-suite runs for release gates or explicit requests. Re-run every `active` case in scope.

- New failure: file or draft a deduplicated defect.
- Existing failure still present: add current evidence to the existing issue.
- Existing failure now passes: record the passing run and, when authorized, comment with the verification evidence. Leave status changes to the owning workflow.
- Blocked or ambiguous case: record it without converting it to a pass or failure.

Finish with a compact summary:

`run <id>: <scope> · total N · pass A / fail B / needs-decision C / blocked D · confirmed fixes E`

Do not call the run complete until every in-scope case has a recorded result, every failure has reviewable evidence, authorized external writes have been read back, and the run log has been appended.
