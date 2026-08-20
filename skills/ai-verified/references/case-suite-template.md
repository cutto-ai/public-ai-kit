# Verification Suite: Feature or workflow name

Use one suite for one coherent feature or workflow. Replace instructional text when creating a real suite.

## Metadata

| Field | Value |
| --- | --- |
| Suite key | A short stable key used in case IDs |
| Status | Draft / Approved / Superseded |
| Owner | Person or role authorized to approve the assertions |
| Target | Product surface, route, device, or workflow |
| Environment | Non-sensitive environment name and build identifier |
| Requirement sources | Links or paths to the current approved sources |
| Test data and reset | Named fixture plus cleanup or reset contract |
| Tracker output | Parent/project/labels and whether issue writes are authorized |
| Created | YYYY-MM-DD |
| Last reviewed | YYYY-MM-DD |

## Scope

Write one sentence describing the behavior this suite verifies. If a proposed case does not fit this sentence, create or use another suite.

## Decision record

| Date | Owner | Decision | Cases affected | Source updated |
| --- | --- | --- | --- | --- |
| YYYY-MM-DD | Name or role | Concise approved decision | CASE-KEY-A1 | Link or path |

## Suite-specific rules

List only rules unique to this feature. Do not copy the generic execution rules from `SKILL.md`.

## Cases

| Case ID | Status | Checkpoint | Approved assertion and source | Procedure | Expected severity |
| --- | --- | --- | --- | --- | --- |
| CASE-KEY-A1 | active | Observable behavior under test | Concise assertion; cite the owning source and decision | Real actions, comparison source, and required evidence | P1 |

Use stable IDs such as `CASE-<SUITE>-A1`. Group letters may represent workflow areas. Once a case ID appears in a run or defect, do not renumber it.

Valid case statuses:

- `draft`: waiting for owner approval;
- `active`: approved and executable;
- `retired`: preserved for history but excluded from new runs.

## Negative scope

List behavior explicitly removed or prohibited for this release. Its absence passes silently; its presence is a failure only when the approved source says so.

## Boundaries

List nearby behavior this suite does not own, including the suite that verifies it when known.

## Open decisions and blockers

| Item | Owner | Decision needed | Affected cases | Status |
| --- | --- | --- | --- | --- |
| Short question | Name or role | Two or three concrete choices | CASE-KEY-A2 | Open |

## Run log

Append rows; never rewrite prior results.

| Run | Date | Build | Case | Result | Evidence or issue | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| r1 | YYYY-MM-DD | Build identifier | CASE-KEY-A1 | pass / fail / needs-decision / blocked | Relative artifact path or tracker link | Relevant environment, decision, or escaped-defect note |
