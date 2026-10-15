# CampusFlow Engineering Understanding Check

This documented question set supports the six-question Engineering Understanding Check required by CampusFlow Next. The interactive CLI version should present one question at a time, validate the selected answer, calculate the score, and display the result. Keep the CLI implementation and this question set aligned.

## Questions

### 1. Why must a rejected operation leave the ticket collection unchanged?

A. So the CLI can avoid printing an error  
B. To preserve data integrity and prevent partial state changes  
C. So ticket IDs are always reset to 1  
D. To make JSON files smaller

**Correct answer:** B

### 2. What should happen when a user tries to add a note to a resolved ticket?

A. Add the note and silently reopen the ticket  
B. Delete the ticket's existing notes  
C. Reject the operation until the ticket is explicitly reopened  
D. Change the ticket to `in_progress`

**Correct answer:** C

### 3. What does AND semantics mean when category and status filters are both supplied?

A. A ticket matches if either filter matches  
B. The category filter is ignored  
C. A ticket must match both the category and status filters  
D. All tickets are returned

**Correct answer:** C

### 4. How should title-substring search behave?

A. It should match only exact, case-sensitive titles  
B. It should match a substring without regard to letter case  
C. It should change the stored title to lowercase  
D. It should search only ticket IDs

**Correct answer:** B

### 5. What is the correct behavior for a legacy JSON ticket that has no `notes` field?

A. Reject every ticket in the file  
B. Silently delete the ticket  
C. Treat the missing notes field as an empty list or otherwise preserve compatibility  
D. Overwrite the entire JSON file with an empty list

**Correct answer:** C

### 6. Why should the full test suite be run after merging a feature branch?

A. To prove that the feature has the largest number of lines  
B. To check that the integrated changes work together and preserve existing behavior  
C. To avoid reviewing the code  
D. To replace the need for regression tests

**Correct answer:** B

## Scoring guidance

- One point per correct answer; maximum score: **6**.
- Suggested result bands: **5–6: Pass**; **3–4: Review recommended**; **0–2: Revisit the design and implementation**.
- The CLI should report the score as `n/6` and show the result band.
- Invalid answers should be handled clearly and must not accidentally count as correct. Whether the CLI retries an invalid answer or records it as incorrect should be consistent with the implementation and its tests.

## Maintenance

When implementation details or shared contracts change, update this document and the CLI question set together. Test all six answer paths, invalid input handling, score boundaries, and result-band boundaries.
