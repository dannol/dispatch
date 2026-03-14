---
id: TASK-088
status: in-progress
priority: high
created: 2026-03-04T16:44:00Z
updated: 2026-03-05T20:35:00Z
assignedTo: gortarin
dependencies: [TASK-022]
blockedBy: []
estimatedEffort: medium
tags: [workstream_design, design, hld, phase-2]
---

# TASK-088: Create Human-Readable HLD from Migration Design v2

## Objective
Create a concise, human-optimized High-Level Design document (~6 pages) distilled from the detailed pbxx-to-vbcs-migration-design-v2, suitable for team decision-making and stakeholder review.

## Context
Design review feedback (Billy, Erick, Andrew) flagged that the 1677-line v2 design is too dense for human review. The detailed v2 remains as the authoritative reference, but a shorter HLD is needed for broader consumption and decision-making.

**Key constraint from gortarin:** Include 1-2 low-level ABC use case slices (e.g., CreateBundle, GetSubmissionStatus) so readers can see what AI-driven implementation looks like at the detail level. The rest should stay high-level.

## Acceptance Criteria
- [ ] Before design review, distill a focused design scoped to features needed to migrate ABC into VBCS — cut non-ABC content to summaries
- [ ] Includes requirements summary table at top
- [x] Includes scope and prioritization section (why PBXX migration, how it ranks vs other problems — must cover: GCRID deadline, Hex deprecation, VCBM deprecation + region flex requirement, and other external obligations)
- [x] Addresses VCBM vs Selection Central sequencing — may need VCBM migration first due to regionflex impact
- [x] Explains how 500 concurrent ORCA workflow fan-out will be handled (bulk creation). Add as new requirement.
- [x] Includes execution model section (AI-driven vs human-required tasks, review cadence)
- [x] Includes 1-2 low-level ABC use case slices showing implementation detail
- [x] Architecture diagrams included (with VBCS boundary box, internal/external distinction)
- [x] Identifies areas needing further low-level design spikes and creates tasks for them
- [x] Notes that VBCS WorkflowState error format must be verified compatible with ABC's frontend error parser (Andrew's actionable error surfacing)
- [x] References v2 as detailed appendix for deep-dives
- [x] All local workspace paths replaced with code.amazon.com links
- [x] Experiment with cross-model review — have a different AI model review the HLD for errors, hallucinations, and gaps

## Implementation Guidance
1. **Load the `writing-designs` skill first** — it contains all accumulated design principles (96+) from prior feedback rounds. Review the checklist and document structure before making changes.
2. Start from v2-collated.md — identify the ~10 most important sections for decision-makers
2. Summarize each into 1-2 paragraphs max
3. Pick 1-2 ABC use cases (suggest: CreateBundle flow, GetSubmissionStatus) and keep their full detail as "implementation slice" examples
4. Add requirements summary table (from TASK-012 requirements)
5. Add scope/prioritization section addressing Alex Swain's feedback
6. Add execution model section addressing Billy's feedback
7. Redraw architecture diagram with VBCS boundary box per Andrew's feedback
8. Find collaborative doc hosting alternative (Quip deprecated)

## Artifacts
- `design/pbxx-to-vbcs-migration-hld.md` — the HLD
- New TASK-* files for each identified low-level design spike

## Validation
- HLD is understandable without reading v2
- Team can make decisions from HLD alone
- Low-level slices give concrete feel for implementation approach

## Notes
---
2026-03-04 16:44 - Created from design review feedback triage item #1. TASK-022 is the parent design spike; this is a follow-on deliverable.

---
2026-03-06 00:05 - SESSION CHECKPOINT — v3 Feedback Incorporation Progress

**Completed feedback items in v3:**
1. ✅ Scope and Prioritization section added (items #3, #5, C25) — after The Problem section
2. ✅ Glossary hallucinations fixed — G2S2 and ORCA expansions removed (item C1/Nick)
3. ✅ "Shadowing" → "gradual traffic dial-up" — all 4 references (item #11/Tommy)
4. ✅ "No DynamoDB direct reads" → "no cross-service DynamoDB direct reads" (item C5/Connor)
5. ✅ Header updated (date, task refs, sub-document names for v3)
6. ✅ GCRID email saved as design resource
7. ✅ HEX deprecation summary saved as design resource (VBCS is on HEX, not PBXX)
8. ✅ Service hosting verified from codebases (VBCS+PBGCS on HEX, rest on Apollo)

**Remaining feedback to incorporate in v3:**
- Add wiki/docs links to glossary (C3/Andrew)
- Clarify Limestone role (C2/Erick)
- Clarify deletion chain — MBWS calls CC directly (C4/Erick)
- Clarify STARFIRE_BRAND = retrofit bundles (C6/Tommy)
- Convert §Section references to markdown anchor links (C11/Andrew)
- Consolidate "not protobuf" language (C22/Andrew)
- Add GCRID campaign doc links (C18/Sajid) — ✅ replied in Slack, still need in design
- Replace local workspace paths with code.amazon.com links (item #14)
- Redraw architecture diagram with VBCS boundary box (item #10/Andrew)
- Clarify terminal states (C12/Alex)
- Clarify autoGenerateContent is deprecated (C13/Erick)
- Clarify content gen for Seller Central — EU away team (C13b/Erick)
- Clarify why no status API in VBCS (C14/Alex)
- Clarify search architecture + vendor-scoped browsing (C19/Erick)
- Explain why no timeline estimates (C21/Erick)
- AI worst-case scenarios — human-authored (C34/Billy)
- Guiding tenets for AI in design (C35b, C35c/Billy)

**Blocked on gortarin input:**
- VCBM deprecation + regionflex story
- Selection Central timeline
- Execution model framing (item #2)
- History page usage check (item #12)
- 500 concurrent workflow handling (item #6)

**Design review Slack actions completed:**
- ✅ Posted update to #ce-tech-ai-tools and #pulse-ai-interest
- ✅ Replied to Sajid's GCRID thread with links
- ✅ Created posting-heartbeat skill
- ✅ Updated design-review-with-slack skill tone

**To resume:** Load managing-tasks skill, read TASK-088. Continue incorporating feedback from the remaining list above. Pick up blocked items when gortarin provides input.

---
2026-03-06 20:32 - SESSION CHECKPOINT — v3 Design Review Feedback Complete

**All team design review feedback addressed:**
- ✅ C3: Glossary links (code.amazon.com, wikis for BUDA/VMP/ORCA/G2S2/PBMS/TA, Limestone added)
- ✅ C9: Keep SC/VC status tracking (product decision with Josh)
- ✅ C11: All §Section refs → markdown anchor links
- ✅ C13/C13b: PBGCS deprecation + BundleContentGenerationService replacement
- ✅ C14: Why no status API in VBCS today
- ✅ C18: GCRID campaign doc links
- ✅ C21: Timeline explanation (AI-first, subsequent review)
- ✅ C22: Protobuf language consolidated
- ✅ C34: AI worst-case scenarios table (human-reviewed)
- ✅ C35b/c: 5 guiding tenets for AI-driven development
- ✅ #2: Execution model — answered in Slack thread (Billy)
- ✅ #6: 500 concurrent workflows — parent ORCA workflow for >10
- ✅ #10: Architecture diagram with VBCS boundary box
- ✅ #12: Default keep history page, pending usage metrics (product decision)
- ✅ #14: Local paths → code.amazon.com
- ⏳ #13 (AC): Cross-model review — deferred to doc-complete

**gortarin feedback items 1-9 all applied:**
1. Header: v3 status, review history
2. proposed-tasks.md in sub-documents
3. Protobuf note moved to How Clients Migrate
4. Scope and Prioritization moved before The Problem + VCBM reframed
5. Follow-On Designs section added
6. Why Now reframed (AI suitability first)
7. Consolidation vs HEX reframed
8. GCRID contingency reframed
9. VCBM in scope, follow-on design

**File reorg:** design/resources/, design/test/, design/v2/, redirect file, proposed-tasks.md
**Skills updated:** writing-designs (principles 64-69), 5 coding/planning skills (tenets)
**Fixed:** Global ~/.gitignore was blocking git add in all repos (core.excludesfile unset)

**Design is at 1152 lines, 17 top-level sections.**
**Next:** Cross-model review (#13), then proposed tasks walkthrough.

**To resume:** Load managing-tasks skill, read TASK-088. The v3 design is ready for cross-model review. Agents can read design/PBXX_HLD/pbxx-to-vbcs-migration-design.md + appendices.

---
2026-03-06 21:19 - Cross-model review experiment (#13 AC) — CLOSED
Result: Not useful. Kimi-K couldn't complete the task. DeepSeek feedback was not actionable.
Conclusion: Cross-model review did not add value for this design document. Marking AC as done (experiment completed, negative result).

---
2026-03-07 19:31 - SKILL OPTIMIZATION ANALYSIS — writing-designs skill de-dupe and restructure plan documented in [TASK-103](TASK-103.md). Key findings: 96 principles can merge to ~35-40 via 15 clusters, checklist 100% duplicates principles, SKILL.md at 31KB violates <500 line guideline. Estimated ~50% token reduction. Ready to implement.
