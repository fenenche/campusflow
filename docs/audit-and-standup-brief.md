# CampusFlow Next — Audit & Stand-up Brief

**Prepared:** 2026-10-15  
**Audience:** Bront888 (Engineer A) and Dorcas / `dinalegwu` (Engineer B)  
**Purpose:** A shared, evidence-based briefing for today's audit and stand-up. Use the checklists live; update outcomes only after the team verifies them.

> **Status rule:** Distinguish *implemented*, *CI passed on a PR head*, *merged*, and *verified on integrated `main`*. These are different claims. Do not claim a review, test run, learning interaction, or approval that has not actually happened.

## 1. Stand-up in 10 minutes

Each person answers, in order:

1. **Done:** What did I personally complete since the last check-in? Link the PR, commit, test, or document.
2. **Evidence:** What proves it works or meets the requirement?
3. **Next:** What is the one task I will finish next?
4. **Blocker:** What do I need from my partner or the repository?
5. **Risk:** What must not be described as complete yet?

### Suggested opening

“We're checking the CampusFlow Next work against the actual repository and sprint criteria. We'll separate merged features from open PRs and CI evidence, assign each remaining item to an owner, and leave with a clear next action. We'll only mark a requirement complete when we can point to evidence.”

## 2. Current verified repository snapshot

Snapshot checked against GitHub PR metadata on 2026-10-15. Re-check before presenting because statuses can change.

| Item | Recorded status | Evidence / what it means |
|---|---|---|
| Original baseline | 38 tests reported by Engineer A | [Baseline record](baseline-check.md). Historical local output; not a new run. |
| Structured notes and persistence validation | Merged | [PR #13](https://github.com/Bront888/campusflow/pull/13). Partner review included change requests, corrections, and approval. |
| Search, combined filters, reports, CLI, understanding check | Merged | [PR #15](https://github.com/Bront888/campusflow/pull/15). CI run [#38598070720](https://github.com/Bront888/campusflow/actions/runs/38598070720) passed on the PR head with 75 tests. This was before merge. |
| Malformed persisted enum values | Open PR; CI passed | [PR #16](https://github.com/Bront888/campusflow/pull/16); [CI run #38625113447](https://github.com/Bront888/campusflow/actions/runs/38625113447) succeeded on its PR head. Dorcas's submitted review is not confirmed in the snapshot. |
| AI learning log | Open PR; Bront draft entries need his own review; Dorcas entries pending | [PR #17](https://github.com/Bront888/campusflow/pull/17). A draft is not the same as completed personal evidence. |
| Baseline/verification documentation | Open PR | [PR #18](https://github.com/Bront888/campusflow/pull/18). Updates the record and explicitly tracks remaining work. |
| Full suite on integrated `main` after outstanding changes | Not verified in this snapshot | Must run and record the actual command, branch, commit, count, and output after accepted changes are integrated. |
| Dorcas's three genuine AI-learning entries | Pending in the record | Dorcas must provide her own real prompts, experiments, independent checks, and outcomes. |
| PR #14 documentation | Merged | [PR #14](https://github.com/Bront888/campusflow/pull/14). Do not imply every PR had a submitted review; #14 and #15 had no submitted review recorded in the earlier audit. |

## 3. Audit checklist

Mark a box only when the evidence is visible and checked.

### Product and implementation
- [ ] Ticket creation, validation, priority, assignment, workflow transitions, reopening, and open queue still work.
- [ ] Ticket notes are structured, validated, persisted, and backward-compatible with legacy records that lack `notes`.
- [ ] Invalid note operations leave the entire ticket collection unchanged.
- [ ] Search is case-insensitive title-substring matching.
- [ ] Category, status, and priority filters combine with AND semantics.
- [ ] Reports cover status, priority, category, resolution percentage, and unresolved tickets, including empty/zero cases.
- [ ] The CLI exposes the added search, notes, reports, and six-question Engineering Understanding Check.
- [ ] JSON storage rejects malformed records clearly, including list/object values for enum fields.

### Test and integration evidence
- [ ] Identify the exact commit being audited.
- [ ] Check GitHub Actions for the relevant commit/PR head; record success or failure precisely.
- [ ] After outstanding changes merge, run on integrated `main`:
  ```bash
  git switch main
  git pull origin main
  git diff --check
  python -m unittest discover -s tests -v
  ```
- [ ] Record the actual test count and output. Do not reuse an earlier PR-head result as proof of a later main run.
- [ ] Confirm invalid operations preserve the complete input collection, not merely one field.
- [ ] Confirm the suite includes at least 14 meaningful tests overall and at least five tests authored by each engineer; verify authorship from actual diffs/commits rather than assuming it.

### Collaboration and review process
- [ ] Each engineer has a substantial PR and at least two focused commits on the relevant work branch, as required by the sprint rubric.
- [ ] Each engineer has reviewed the partner's PR with at least two specific observations/questions.
- [ ] Any blocking feedback is addressed, and approval is recorded before merge; nobody approves their own PR.
- [ ] Record real authorship and review evidence. Do not retroactively imply that an open PR was reviewed or approved.
- [ ] Check branch divergence before integrating an old branch; do not blindly merge duplicate/stale work.

### AI-learning evidence
- [ ] Bront reviews and personalizes his own drafted entries in [PR #17](https://github.com/Bront888/campusflow/pull/17).
- [ ] Dorcas writes at least three entries based on her own genuine interactions.
- [ ] Each entry contains the actual prompt/question, idea tested, experiment/application, independent verification, and outcome in the author's own words.
- [ ] At least one team entry records a real, independently verified correction/rejection of an AI suggestion. The PR #13 review/correction trail is relevant evidence; check that the log explains what was corrected and how it was verified.
- [ ] Do not invent prompts, tests, learning reflections, or verification.

## 4. Proposed ownership and next actions

| Owner | Immediate action | Done means |
|---|---|---|
| Bront (Engineer A) | Review and personalize his three AI-log drafts | The first-person outcomes accurately reflect his experience; changes are committed on the log PR. |
| Bront (Engineer A) | Prepare/execute integrated-main verification after merges | Actual command output and commit SHA are recorded in the baseline log. |
| Dorcas (Engineer B) | Independently review PR #16 | Submitted review with specific findings; request changes if needed, or approve only if justified. |
| Dorcas (Engineer B) | Add three genuine AI-learning entries | Her own prompts, experiments, independent checks, and outcomes are committed; no one writes these for her. |
| Both | Audit review/commit/test attribution against the rubric | Evidence-backed checklist, gaps assigned to an owner, no unsupported completion claims. |

These are proposed actions based on the current record; update owners if the pair agrees otherwise during stand-up.

## 5. PR conversation links

- [PR #13 — structured notes and storage validation](https://github.com/Bront888/campusflow/pull/13)
- [PR #14 — documentation update](https://github.com/Bront888/campusflow/pull/14)
- [PR #15 — search, reports, CLI and understanding check](https://github.com/Bront888/campusflow/pull/15)
- [PR #16 — malformed stored enum field types](https://github.com/Bront888/campusflow/pull/16)
- [PR #17 — AI learning log](https://github.com/Bront888/campusflow/pull/17)
- [PR #18 — baseline and verification log](https://github.com/Bront888/campusflow/pull/18)

## 6. Audit notes to fill in during the session

**Audit date/time:**  

**Commit/branch inspected:**  

**CI run and result:**  

**Integrated-main test command/output:**  

**Requirements verified complete:**  

**Gaps or discrepancies found:**  

**Decisions made together:**  

**Action / owner / due time:**
- 
- 
- 

**Partner review evidence/links:**  

**Next check-in:**  

---

## 7. Closing statement

“Before we close, we have named an owner for every open requirement, linked the evidence we actually checked, and recorded what remains unverified. We will not call the sprint fully complete until the required reviews, genuine learning entries, and integrated-main test evidence are all present.”
