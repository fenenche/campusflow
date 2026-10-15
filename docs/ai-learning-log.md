# AI Learning Log

This file records AI-assisted work with links to project evidence. The Engineer A entries are drafted from recorded conversation and GitHub activity; Bront888 must review the reflections and edit them into his own words before submission. Dorcas must write her own entries. Do not invent prompts, experiments, or evidence.

## Engineer A — Bront888

### Entry 1 — Audit requirements against repository evidence

- **Date:** 2026-10-14
- **Actual prompt:** “Inspect the requirements, cross-check the progress and tell me and point out what is left to final completion.”
- **AI idea tested:** Check implementation, CI, review history, contribution evidence, and learning-log requirements separately rather than assuming merged features mean every requirement is complete.
- **Experiment/application:** Inspected PRs #13–#15 and compared Dorcas’s original feature branch with current main. The branch had diverged, so it was not merged blindly.
- **Independent verification:** PR #15's CI passed with 75 tests on its PR head. GitHub PR and branch records support the review and divergence findings. This was not a post-merge main test.
- **Outcome — personalize before submission:** The audit showed that passing tests alone do not prove individual authorship, reciprocal review, or completed learning logs.
- **Correction/rejection:** Rejected the assumption that the sprint was fully complete merely because the features were merged and the PR CI passed.
- **Evidence:** https://github.com/Bront888/campusflow/pull/13 · https://github.com/Bront888/campusflow/pull/14 · https://github.com/Bront888/campusflow/pull/15

### Entry 2 — Correct note invariants after review

- **Date:** 2026-10-14
- **Actual prompt:** “edit my docs and i think there's one file they want us to create”
- **AI idea tested:** Inspect the existing docs and sprint issue to identify the missing Engineering Understanding Check artifact, while keeping documentation aligned with the code.
- **Experiment/application:** The notes implementation was submitted in PR #13. Dorcas requested changes for the resolved-ticket guard and malformed existing notes; the implementation and tests were updated before approval.
- **Independent verification:** PR #13's review history records changes requested followed by approval of the updated head. The updated branch's reported test output was 53 tests passing. The six-question check was also tested in the integrated PR #15 run.
- **Outcome — personalize before submission:** AI-assisted code needs to be checked against the actual invariants. Reviewer feedback exposed cases that needed explicit guards and regression tests.
- **Correction/rejection:** The initial notes implementation was not treated as finished; the resolved-ticket and malformed-notes cases were corrected before approval. This is a documented correction to AI-assisted implementation based on human review.
- **Evidence:** https://github.com/Bront888/campusflow/pull/13 · https://github.com/Bront888/campusflow/blob/main/docs/engineering-understanding-check.md

### Entry 3 — Validate malformed stored enum fields

- **Date:** 2026-10-14
- **Actual prompt:** “I am not on my PC now but you can code directly for me and then let me know when we need to communicate to my partner”
- **AI idea tested:** Inspect the storage validator for malformed JSON values that could cause raw exceptions instead of the expected StorageError.
- **Experiment/application:** Added string-type guards for category, urgency, priority, and status, plus regression cases for list and object values across all four fields. Opened PR #16.
- **Independent verification:** GitHub Actions run #38625113447 passed on PR #16's head. This is CI evidence; no local test run is claimed.
- **Outcome — personalize before submission:** Validate a value's type before operations that assume it is a string or hashable. Regression tests make the malformed-input cases reproducible.
- **Correction/rejection:** Rejected the unsafe assumption that parsed JSON enum fields are necessarily strings; added type checks and regression tests.
- **Evidence:** https://github.com/Bront888/campusflow/pull/16 · https://github.com/Bront888/campusflow/actions/runs/38625113447

## Engineer B — Dorcas (`dinalegwu`)

**Pending: Dorcas must complete this section herself.** Add three genuine interactions using her actual prompts, experiments, independent verification, and outcomes in her own words. Do not attribute Bront888's interactions to her.

### Entry template

- **Date/time:**
- **Actual prompt or question:**
- **AI response or idea tested:**
- **Experiment or application:**
- **Independent verification:**
- **Outcome in my own words:**
- **Correction/rejection (if applicable):**
- **Evidence:**

## Completion status

- Engineer A: three evidence-linked draft entries; Bront888 must personalize the reflections before submission.
- Engineer B: three genuine entries still required.
- Team correction/rejection: a correction to AI-assisted implementation is documented above; confirm with the evaluator that this satisfies the wording of the requirement.
- PR #16: CI passed, but do not describe the PR as merged; independent review was still pending when this log was drafted.
