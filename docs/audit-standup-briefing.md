# CampusFlow Next — Audit & Stand-up Briefing

**Prepared:** 2026-10-15  
**Repository:** [Bront888/campusflow](https://github.com/Bront888/campusflow)  
**Purpose:** Shared briefing for Engineer A and Engineer B before the audit and stand-up.  
**Status note:** This document reflects the GitHub records checked on 2026-10-15. It is a working briefing, not a claim that every acceptance criterion is complete.

## 1. Thirty-second project summary

CampusFlow is a standard-library Python command-line ticket tracker. The CampusFlow Next sprint extended the existing app with structured ticket notes, defensive JSON validation, case-insensitive title search, combined filters, richer reports, a six-question Engineering Understanding Check, CLI access to new features, regression tests, and GitHub Actions CI.

The architecture remains intentionally small: `main.py` handles CLI interaction; `campusflow/` contains business logic, workflow, storage, search, and reporting; `tests/` holds `unittest` tests; and `docs/` records design contracts, baseline evidence, the learning log, and the understanding-check material.

**Current truth:** The main feature PRs #13 and #15 are merged. PR #16's storage-hardening CI passed but its independent review and merge are not confirmed. PR #17 (AI-learning log) and PR #18 (baseline verification log) are open. A post-merge full-suite run on the final integrated `main` is still required.

## 2. What we have accomplished

### Core features and reliability

- Preserved the existing ticket tracker and its Python standard-library / `unittest` approach.
- Added structured notes with trimmed author/message fields, validation, and protection against adding notes to resolved tickets until they are reopened.
- Added persisted-note validation while retaining backward compatibility for older records that have no `notes` field.
- Added case-insensitive title-substring search.
- Added category, status, and priority filters with AND semantics when multiple filters are supplied.
- Extended reports with category counts, resolution percentage, and unresolved-ticket counts while preserving prior report information.
- Added CLI access for search/filtering, notes, reports, and the six-question Engineering Understanding Check.
- Added focused regression tests and a GitHub Actions test workflow.
- Identified and prepared a further storage-hardening fix for malformed JSON enum fields: list/dict values should become a clear `StorageError`, not leak a raw `TypeError`.

### Documentation and engineering process

- Documented the original baseline and its limits.
- Recorded the architecture, data model, priority algorithm, workflow invariants, persistence expectations, and shared function contracts.
- Created the Engineering Understanding Check document.
- Started the AI-learning log. Bront's entries are drafts linked to real project records and must be reviewed/personalized by Bront; Dorcas must add her own genuine entries.
- Kept unverified local runs, approvals, and partner activity explicitly unclaimed.

## 3. Evidence and PR status

| Item | Current status | Evidence / interpretation |
|---|---|---|
| Baseline record | Merged | [PR #12](https://github.com/Bront888/campusflow/pull/12); original local baseline was reported as 38 tests passing. |
| Notes + storage validation | Merged | [PR #13](https://github.com/Bront888/campusflow/pull/13), merge commit `a7d31c94bbdacf68958530b8456a2537b5a46dac`. Dorcas submitted specific change requests on the earlier version; the resolved-ticket guard and malformed-notes handling were corrected before her approval. |
| Sprint documentation | Merged | [PR #14](https://github.com/Bront888/campusflow/pull/14). |
| Search, reports, CLI, understanding check | Merged | [PR #15](https://github.com/Bront888/campusflow/pull/15), squash merge commit `b5d5435552e95f7501739f719aa49729fe7abbb9`. |
| Test suite on PR #15 head | Passed | [Actions run #38598070720](https://github.com/Bront888/campusflow/actions/runs/38598070720): `Ran 75 tests ... OK`. This is PR-head evidence before merge, not a post-merge `main` run. |
| Malformed enum-type hardening | Open; CI passed | [PR #16](https://github.com/Bront888/campusflow/pull/16). [Actions run #38625113447](https://github.com/Bront888/campusflow/actions/runs/38625113447) concluded success for head `0efdbc35645cca31ebdeb17a05a251dbe1a2ccd3`. Partner review/merge not confirmed. |
| AI-learning log | Open | [PR #17](https://github.com/Bront888/campusflow/pull/17). Bront entries need personal review; Dorcas's own entries remain outstanding. |
| Baseline/verification log update | Open | [PR #18](https://github.com/Bront888/campusflow/pull/18). It records the status accurately; it does not mean final integration tests have run. |

### Test evidence: say exactly this

- Original baseline: Engineer A supplied local output showing **38 tests passed**. It was recorded as user-supplied output, not independently run by the assistant.
- PR #15 head: GitHub Actions reported **75 tests passed** before merge.
- PR #16 head: GitHub Actions **conclusion: success**. The action summary checked here does not itself provide a test count.
- Final integrated `main`: **post-merge full-suite result not yet confirmed**. Do not state that the final integrated suite has passed until the command is run on the final commit and its output is recorded.

## 4. Architecture and rules to be able to explain

- **CLI boundary:** `main.py` gathers input, calls business functions, and turns expected exceptions into user-readable messages. Business logic should be testable without interactive prompts.
- **Persistence:** JSON files; missing file means a fresh empty collection. Malformed JSON or invalid records should fail clearly rather than silently discard data.
- **Ticket notes:** `add_note(tickets, ticket_id, author, message)`; unknown ID raises `KeyError`; invalid inputs or malformed in-memory notes raise `ValueError`; persisted invalid notes raise `StorageError`. Rejected operations should leave the collection unchanged.
- **Legacy compatibility:** Records without a `notes` field remain loadable.
- **Search:** title uses case-insensitive substring matching. Multiple filters combine with AND, not OR. Search must not mutate/reorder the source collection.
- **Workflow invariant:** allowed forward transitions are `open -> in_progress -> resolved`; a ticket must be assigned before entering `in_progress`; a resolved ticket must be explicitly reopened before mutation.
- **Storage hardening under review:** check the type of enum-like fields before membership checks, because lists/dictionaries are unhashable and can otherwise trigger `TypeError`.
- **Tests:** use Python's standard-library `unittest`; run the whole suite, not only a new test module.

## 5. Outstanding checklist for the audit

- [ ] Dorcas independently reviews PR #16, records specific findings, and the author addresses any blocking feedback.
- [ ] PR #16 is merged only after the required review/approval and checks.
- [ ] PR #17: Bront reads and personalizes his entries so they accurately reflect his own learning and outcomes.
- [ ] PR #17: Dorcas contributes at least three real AI interactions with her own prompts, experiments, independent verification, and outcomes. Do not invent these for her.
- [ ] Confirm whether the evaluator accepts the documented human-review correction as satisfying the team requirement for a verified correction/rejection of an AI suggestion; if not, document a genuine explicit rejection/correction with evidence.
- [ ] PR #18 gets a factual review and is merged after review.
- [ ] Reconcile branches/PRs; do not merge Dorcas's old divergent implementation branch blindly because its search/report work overlaps already merged code.
- [ ] On the final integrated `main`, run:
  
  ```bash
  git switch main
  git pull origin main
  git diff --check
  python -m unittest discover -s tests -v
  ```

- [ ] Record the date, final commit SHA, exact command, and actual output in `docs/baseline-check.md`.
- [ ] Confirm test authorship evidence (at least five meaningful tests per engineer) and the required focused commits/PRs per engineer from GitHub history; do not infer authorship solely from a merged feature.
- [ ] Confirm reciprocal review evidence: substantive review observations/questions, response to blocking feedback, and approval before merge. Do not imply review occurred unless GitHub shows the submitted review.

## 6. Suggested stand-up agenda (10–15 minutes)

1. **Shared status (2 min):** summarize merged features and the 75-test PR-head result.
2. **Reliability fix (3 min):** Dorcas reviews PR #16; discuss whether the enum type guards preserve valid stored data and reject malformed values consistently.
3. **Evidence and learning log (3 min):** each engineer confirms which genuine interactions they can document and which verification they personally performed.
4. **Final integration (3 min):** agree who will run the full suite on final `main`, capture the output, and update the baseline record.
5. **Ownership and close-out (2–4 min):** assign a person and evidence artifact to every unchecked item; avoid marking any item done without proof.

## 7. Questions you should be ready to answer

**Why keep this as a CLI / standard-library app?**  
The documented scope requires a small Python command-line tracker, standard-library implementation, JSON persistence, and `unittest`. The sprint extends the existing architecture rather than redesigning it.

**Why do filters use AND semantics?**  
When a user supplies category, status, and priority together, the result should satisfy every supplied criterion; otherwise the filter combination would be ambiguous and return broader matches than requested.

**Why validate persisted data if the app already validates user input?**  
JSON can be edited, corrupted, or created by older versions outside the normal input path. Loading must validate stored records too, and should report malformed data clearly instead of crashing unpredictably or silently discarding it.

**Why allow missing notes on older records?**  
That preserves compatibility with tickets saved before notes were introduced. If a notes field is present, it must meet the new schema.

**What does “75 tests passed” prove?**  
It proves the suite passed on the PR #15 head at that point. It does not prove the final post-merge `main` suite passed, nor does it establish each engineer's test authorship or required review evidence.

**What is still blocking a clean completion claim?**  
Partner review/integration for PR #16, completion of genuine learning-log entries for both engineers, final `main` test evidence, and confirmation of authorship/commit/review requirements.

**What should we not claim?**  
Do not claim PR #16 is merged, do not claim the final integrated suite has passed, do not claim Dorcas submitted reviews that are not visible in GitHub, and do not fabricate personal learning entries or test authorship.

## 8. Shared action tracker

| Action | Owner | Evidence required |
|---|---|---|
| Review PR #16 with specific observations | Dorcas | Submitted GitHub review |
| Address review feedback and merge when approved | Bront / PR author | Updated commits, checks, approved review, merge record |
| Review/personalize Bront's AI log entries | Bront | Accurate first-person entries on PR #17 |
| Add three genuine AI learning entries | Dorcas | Her own authored changes and verifiable examples |
| Review the baseline log facts | Dorcas | Review on PR #18 or documented factual correction |
| Run final full suite on integrated main | Agree during stand-up | Command output, branch and SHA recorded in baseline log |
| Audit test authorship and commit counts | Both | GitHub commit/test history mapped to each engineer |
| Check all sprint acceptance criteria | Both | Checklist with evidence links, not verbal assumptions |

## 9. Links to keep open during the meeting

- [Repository](https://github.com/Bront888/campusflow)
- [PR #13 — notes/storage validation](https://github.com/Bront888/campusflow/pull/13)
- [PR #15 — search/reports/CLI](https://github.com/Bront888/campusflow/pull/15)
- [PR #16 — malformed storage field types](https://github.com/Bront888/campusflow/pull/16)
- [PR #17 — AI-learning log](https://github.com/Bront888/campusflow/pull/17)
- [PR #18 — baseline verification log](https://github.com/Bront888/campusflow/pull/18)
- [75-test CI run](https://github.com/Bront888/campusflow/actions/runs/38598070720)
- [PR #16 CI run](https://github.com/Bront888/campusflow/actions/runs/38625113447)
- [Design decisions](design-decisions.md)
- [Baseline check](baseline-check.md)
- [Engineering Understanding Check](engineering-understanding-check.md)
- [AI learning log](ai-learning-log.md)
