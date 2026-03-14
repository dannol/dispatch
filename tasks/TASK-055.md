---
id: TASK-055
status: in-progress
priority: high
created: 2026-02-19T18:10:00Z
updated: 2026-03-06T03:57:00Z
assignedTo: gortarin
dependencies: [TASK-022]
blockedBy: []
estimatedEffort: small
tags: [workstream_implement, vbcs, datapath, attributes, implementation, phase-1]
skills: [datapath-coding, analyzing-codebases]
---

# TASK-055: Extend VBCS Datapath simpleAttributes to Include All 21 PBXX Rollup Attributes

## Objective
Add the 13 missing rollup attributes to `simpleAttributes.dp` so VBCS Datapath returns all 21 attributes required by PBXX for bundle catalog submission.

## Context
TASK-012 identified that VBCS Datapath only rolls up 8 of the 21 attributes PBXX requires (REQ-023). The fix is straightforward — extend the attribute list in `simpleAttributes.dp`. This unblocks attribute rollup for the migration and addresses REQ-023 directly.

**Note:** VBCS also has `ingredients` in `aggregateMultiValueAttributes.dp`, but that is NOT one of the 21 PBCS rollup attributes (it's VBCS-specific). So the correct count is 8/21 covered, 13 missing.

**Requirements addressed:**
- REQ-023: Component Attribute Aggregation (21 Attributes) — ❌ NOT met → ✅ Met
- Supports REQ-037: Bundle Management Attributes (partial — Datapath attribute availability)

## Files to Read (Context)

### VBCS Datapath source (the file to modify):
- `/home/gortarin/workspace/VirtualBundleCatalogServiceDatapath/src/VirtualBundleCatalogServiceDatapath/src/virtualbundlecatalogservice/internal/rollup/simpleAttributes.dp`

### VBCS Datapath documentation:
- `code-doc/VBCS/VBCS-datapath.md` — Full view documentation including attribute gap analysis
- `code-doc/Datapath/overview.md` — Datapath Query Language basics

### VBCS Datapath test files:
- `/home/gortarin/workspace/VirtualBundleCatalogServiceDatapath/src/VirtualBundleCatalogServiceDatapath/tst/virtualbundlecatalogservice/internal/testRollupAttributes.dp`
- `/home/gortarin/workspace/VirtualBundleCatalogServiceDatapath/src/VirtualBundleCatalogServiceDatapath/test-data/virtualbundlecatalogservice/internal/testDataRollupAttributes.dp`

### Parent view that calls simpleAttributes:
- `/home/gortarin/workspace/VirtualBundleCatalogServiceDatapath/src/VirtualBundleCatalogServiceDatapath/src/virtualbundlecatalogservice/internal/rollupAttributes.dp`

### Requirements reference:
- `requirements/pbxx-to-vbcs-requirements-table.md` — REQ-023 details

### PBXX reference (what attributes are needed):
- `code-doc/PBXX/PBCS/PBCS-analysis.md` — PBCS rollup attribute list

## Acceptance Criteria
- [ ] `simpleAttributes.dp` updated with all 21 attributes
- [ ] Datapath tests updated to cover new attributes
- [ ] Tests pass in Datapath Sandbox
- [ ] No regression on existing 8 attributes

## Implementation Guidance

### Current attributes in `simpleAttributes.dp` (8):
```
brand, display_on_website, generic_keyword, gl_product_group_type,
product_category, product_subcategory, product_type, subject_keyword
```
Plus `ingredients` in `aggregateMultiValueAttributes.dp` (separate file, NOT one of the 21 PBCS attributes).

### Missing attributes to add (13):
Verified against `ProductBundleCatalogService.cfg` → `*.*.rollupAttributes`:
```
brand_code, browse_node_id, deprecated_retail_ordering_channel, display_attribute,
handling_group, item_type_keyword, manufacturer_vendor_code, recommended_browse_nodes,
replenishment_strategy, rtip_deprecated_search_terms, rtip_deprecated_subject_keywords,
rtip_tax_class, vendor_name
```

### Steps:
1. Read `simpleAttributes.dp` and understand the pattern
2. Add the 13 missing attribute names to the `attributes` list
3. Determine if any of the 13 are multi-valued (should go in `aggregateMultiValueAttributes.dp` instead)
4. Update test data in `testDataRollupAttributes.dp` to include new attributes
5. Update test in `testRollupAttributes.dp` to verify new attributes
6. Validate in Datapath Sandbox: https://datapath.amazon.com/editor.jsp

### Important Notes:
- The wrapper `itemAttribute` calls `catalog::item::attribute` — verify each new attribute name is a valid catalog attribute
- Some attributes may not exist for all ASINs — the view already handles this (filters out empty results with `(not (list::length values 0))`)
- `recommended_browse_nodes` and `rtip_deprecated_search_terms`/`rtip_deprecated_subject_keywords` may be multi-valued — check if they should go in `aggregateMultiValueAttributes.dp`

### PBCS Source of Truth:
- Config file: `ProductBundleCatalogService/src/ProductBundleCatalogService/configuration/brazil-config/app/ProductBundleCatalogService.cfg`
- Key: `*.*.rollupAttributes` — lists exactly 21 attributes
- Business logic: `BundleAttributesService.rollupAttributes()` — copies from base component if not already present

## Artifacts
- Modified: `src/virtualbundlecatalogservice/internal/rollup/simpleAttributes.dp`
- Possibly modified: `src/virtualbundlecatalogservice/internal/rollup/aggregateMultiValueAttributes.dp`
- Modified: `tst/virtualbundlecatalogservice/internal/testRollupAttributes.dp`
- Modified: `test-data/virtualbundlecatalogservice/internal/testDataRollupAttributes.dp`

## Validation
- Datapath Sandbox test passes
- `brazil-build test` passes in VirtualBundleCatalogServiceDatapath package
- All 21 attributes returned when querying rollupAttributes view

## Notes
---
2026-03-05 23:55 - Claimed by gortarin.

---
2026-03-06 03:45 - Pre-work: Created `datapath-coding` skill to enable AI-assisted Datapath development.
- Read all 7 Datapath code-doc files + canonical wiki (https://w.amazon.com/bin/view/Datapath/QueryLanguage)
- Read VBCS Datapath source files (simpleAttributes.dp, aggregateMultiValueAttributes.dp, rollupAttributes.dp, wrappers, tests, test data)
- Created skill with 3 files (125 + 198 + 177 = 500 lines):
  - SKILL.md — core DQL syntax, view writing, testing patterns
  - references/dql-language-reference.md — complete operator reference from wiki
  - references/vbcs-datapath-patterns.md — VBCS conventions extracted from actual codebase
- Registered in pulse-ai-agent.agent-spec.json
- Task itself (extending simpleAttributes) not yet started — skill creation was prerequisite tooling work
---

---
2026-03-06 04:00 - Workspace created: `~/workspace/VBCSDP_TASK-055`
- Branch: `feature/TASK-055-extend-simple-attributes`
- Updated datapath-coding skill with workspace setup + branch workflow sections

---
2026-03-06 04:07 - Implementation plan finalized after context gathering:

**VBCS Java — NO changes needed:**
- `DatapathGatewayAccessor.getRollupAttributes()` returns `Map<String, IonValue>` — generic, no hardcoded attribute names
- `RollupAttributesManager.rollupAttributes()` iterates all keys and copies to bundle — fully pass-through
- New Datapath attributes will automatically flow through to catalog submission

**Files to modify (all in workspace `~/workspace/VBCSDP_TASK-055/src/VirtualBundleCatalogServiceDatapath`):**
1. `src/.../rollup/simpleAttributes.dp` — add 13 attributes to the list
2. `test-data/.../rollup/testDataSimpleAttributes.dp` — add override branches for new attributes
3. `tst/.../rollup/testSimpleAttributes.dp` — update test case 1 expected output

**Files NOT modified:**
- `aggregateMultiValueAttributes.dp` — PBCS uses first-wins from base component, not cross-ASIN aggregation
- `rollupAttributes.dp` — parent view merges generically, picks up new attributes automatically
- `testRollupAttributes.dp` / `testDataRollupAttributes.dp` — test at rollup level mocks simpleAttributes directly

**Testing:**
1. `brazil-build test` — unit tests must pass
2. Sandbox (human, browser) — verify each new attribute name is valid via `catalog::item::attribute`
3. CR description will note VBCS Java pass-through behavior

---
2026-03-06 14:55 - IMPORTANT FINDING: PBCS uses a different Datapath view for attribute rollup.
- PBCS calls `psd/pba/helpers/getAsinProductDetails` (from ProductBundleDatapathClient package)
- This returns a full product details IonStruct with ALL attributes as top-level keys
- PBCS then iterates the 21 rollup attribute names from config and copies from that struct
- VBCS uses `catalog::item::attribute` which queries attributes one at a time
- 6 attributes not found via `catalog::item::attribute` even on vendor ASINs:
  browse_node_id, replenishment_strategy, rtip_deprecated_search_terms,
  rtip_deprecated_subject_keywords, rtip_tax_class, vendor_name
- These may only be available through the psd/pba product details view
- DECISION NEEDED: Should we switch to the psd/pba view, or are these 6 attributes
  genuinely not needed for VBCS bundles (which are virtual bundles, not product bundles)?
- https://code.amazon.com/reviews/CR-258383153
- brazil-build test: 48 tests, 0 errors
- NOT published — awaiting author review + sandbox testing

## Workspace Cleanup
- Workspace: `~/workspace/VBCSDP_TASK-055`
- **Action required (human):** Once the CR is merged, delete this workspace:
  ```bash
  rm -rf ~/workspace/VBCSDP_TASK-055
  ```
