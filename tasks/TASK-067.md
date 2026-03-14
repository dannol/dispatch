---
id: TASK-067
status: completed
priority: high
created: 2026-02-24T04:44:00Z
updated: 2026-02-26T00:01:00Z
assignedTo: kiro-ai-assistant
dependencies: []
blockedBy: []
estimatedEffort: medium
tags: [vbcs, git-hooks, tooling, mainline, code-quality]
---

# TASK-067: Migrate pulse-ai Git Hooks to VBCS Mainline

## Objective
Bring the pre-commit git hooks developed on the pulse-ai branch into VBCS mainline and update the vbcs-code-writing skill to document them.

## Context
The pulse-ai branch has pre-commit hooks (`.githooks/pre-commit`, `scripts/check-coverage.py`) that enforce ≥95% JaCoCo coverage on modified source files. These hooks are currently only on the pulse-ai branch and are not available to mainline developers. Per ADR-017, all development should happen on mainline, so the hooks need to move there.

Additionally, the vbcs-code-writing skill references these hooks but they don't exist on mainline yet, making the skill documentation misleading.

## Acceptance Criteria
- [x] Review hooks on pulse-ai branch: `.githooks/pre-commit` and `scripts/check-coverage.py`
- [x] Determine if hooks need modification to work on mainline (no pulse-ai-specific logic)
- [x] Add hooks to VBCS mainline via CR
- [x] Update `vbcs-code-writing` skill to reflect correct hook setup instructions for mainline
- [x] Verify hooks work correctly on mainline with `brazil-build`
- [x] CR submitted and approved
- [x] Changes pushed to VBCS mainline

## Implementation Guidance
1. Review hooks on pulse-ai: `git show pulse-ai:.githooks/pre-commit` and `git show pulse-ai:scripts/check-coverage.py`
2. Check if `brazil-build` generates the coverage report at the expected path
3. Strip any pulse-ai-specific logic from hooks
4. Add to mainline via feature branch + CR
5. Update skill with correct setup instructions (`git config core.hooksPath .githooks`)

## Artifacts
- `ai-tools/pre-commit` (added to mainline)
- `ai-tools/check-coverage.py` (added to mainline)
- `ai-tools/README.md` (added to mainline)
- `vbcs-code-writing` skill (updated)

## Notes
---
2026-02-24T21:12:00Z - Recreated from TASK-067 which was accidentally deleted in commit 66abb9d. Notes from TASK-067 session ported below.

---
2026-02-24T17:54:37Z - Claimed by kiro-ai-assistant

---
2026-02-24T17:54:37Z - PLANNING COMPLETE

### Findings from pulse-ai branch

**`.githooks/pre-commit`** does four things:
1. Branch guard: `if [ "$BRANCH" != "pulse-ai" ]; then exit 0; fi` — **removed** for mainline; replaced with mainline guard
2. AI test change detection — **removed**; AI tests now part of standard `brazil-build` (TASK-061)
3. Trailing whitespace removal: `sed -i ''` (macOS) — **fixed** to `sed -i` for Linux
4. Tab character check — **kept as-is**
5. JaCoCo coverage check — **kept as-is**

**`.githooks/check-coverage.py`** (lives in `.githooks/`, not `scripts/` as task description says):
- Searches `../../build/**/coverage-report.xml` — correct for Brazil workspace layout
- No pulse-ai-specific logic — kept verbatim

**`vbcs-code-writing` SKILL.md**: added one-time setup block under Pre-Commit Requirements.

### Folder decision
Used `ai-tools/` at same level as `configuration/`. Future-proof name (tools may outlive Pulse AI). Setup: `git config core.hooksPath ai-tools`.

### Files created/modified

| File | Action |
|------|--------|
| `ai-tools/pre-commit` | Created — mainline guard, whitespace fix, tab check, coverage check |
| `ai-tools/check-coverage.py` | Created — verbatim from pulse-ai |
| `ai-tools/README.md` | Created — setup instructions and feature descriptions |
| `vbcs-code-writing/SKILL.md` | Updated — added `git config core.hooksPath ai-tools` setup block |

---
2026-02-24T18:58:00Z - CR submitted: https://code.amazon.com/reviews/CR-256211635/revisions/1
Branch: feature/TASK-067-ai-tools-git-hooks (still valid, CR is open)

---
2026-02-24T23:48:00Z - CR comment received: Bandit B314 warning on ET.parse() in check-coverage.py.
File parses local JaCoCo build artifact (not untrusted input), so this is a false positive.
Next step: switch to feature/TASK-067-ai-tools-git-hooks, add `# nosec B314 - local JaCoCo build artifact, not untrusted input` to the ET.parse() line, amend commit, update CR.
--- Because 7 8 9. Why was TASK-067 afraid of TASK-075? Because another agent ate it.
---
Agent Context: Logged "Rev 2" in CR revision history after description-only edits
Human Input: Description edits don't create revisions — only code pushes do. Skill already documents this rule.
Learning: Read the revision history rule in vbcs-code-writing skill before logging revisions
---

---
2026-02-25T22:06:00Z - WORKSPACE REBUILT
- Created fresh workspace: `~/workspaces/src/VirtualBundleCatalogService`
- Cherry-picked CR-256211635 commit onto mainline (63c5ab9)
- Feature branch: `feature/TASK-067-ai-tools-git-hooks`
- Mainline: clean at d56b091
- Git hooks configured: `git config core.hooksPath ai-tools`
- Next: address Bandit B314 comment, amend commit, update CR

---
2026-02-25T22:44:00Z - WORKSPACE RECREATED (by the book)
- Deleted old non-standard workspace at ~/workspaces
- Created proper Brazil workspace: `brazil workspace create --name VBCS_TASK-067`
- Location: `~/VBCS_TASK-067/src/VirtualBundleCatalogService`
- brazil-build: PASSED
- check-coverage.py tested: finds report, parses correctly, exits 0
- Pre-commit hook tested: ran during commit, all checks passed
- Added `# nosec B314` to ET.parse() line (addresses CR comment)
- CR updated: https://code.amazon.com/reviews/CR-256211635/revisions/2 (Rev 2: nosec B314 fix, rebuilt from proper workspace)

---
2026-02-26T00:01:00Z - TASK COMPLETED
- CR-256211635 merged to mainline
- Final changes: dropped defusedxml try/except fallback, used defusedxml directly as hard dependency
- Pre-commit hook checks for defusedxml and gives clear install instructions if missing
- README expanded with AI-assisted development context and defusedxml rationale
- Workspace `~/VBCS_TASK-067` deleted
