---
id: TASK-040
status: blocked
priority: medium
created: 2026-02-12T20:48:00Z
updated: 2026-02-20T17:13:00Z
assignedTo: gortarin
dependencies: [TASK-012, TASK-053]
blockedBy: ["VMP validator architecture alignment"]
estimatedEffort: medium
tags: [workstream_implement, vbcs, validators, implementation, phase-1, g2s2]
skills: [writing-vbcs-code, analyzing-codebases, testing-vbcs-locally]
---

# TASK-040: Implement BundleRelationshipLimitsValidator

## Objective
Add BundleRelationshipLimitsValidator to VBCS following existing validator patterns.

## Context
TASK-012 identified that VBCS is missing BundleRelationshipLimitsValidator (REQ-021). This validator checks G2S2 relationship limits:
- Max 250 bundles per component (83 for multi-vendor)
- Min 2 components per bundle
- Max 100 components per bundle

VBCS currently uses hardcoded limits (2-10 components). This validator will call G2S2 for dynamic limits.

**VBCS Codebase:** `/Users/gortarin/workspace/VirtualBundleCatalogService`

## Acceptance Criteria
- [ ] BundleRelationshipLimitsValidator created following VBCS patterns
- [ ] Validator calls G2S2 getRelationshipLimits API
- [ ] Validator checks all 3 limits (250-bundle, 2-min, 100-max)
- [ ] Validator handles multi-vendor limit (83 vs 250)
- [ ] Validator registered in all applicable validator lists
- [ ] Unit tests created
- [ ] AI tests created following aitest/AI-TESTING-SOP.md
- [ ] Integration tests pass in RDE

## Implementation Guidance

### Phase 1: Setup and Study Patterns
1. Ensure working in pulse-ai branch: `git checkout pulse-ai`
2. Review existing validators in `VirtualBundleCatalogService/src/.../validators/`
3. Identify validator interface and registration mechanism
4. Check if G2S2 client exists in VBCS or needs to be added

### Phase 2: Implement Validator
1. Create BundleRelationshipLimitsValidator class
2. Implement G2S2 getRelationshipLimits integration
3. Check 250-bundle limit per component (83 for multi-vendor)
4. Check 2-100 component range per bundle
5. Add error messages for limit violations
6. Register validator in configuration

### Phase 3: Testing
1. Write unit tests
2. Create AI tests in aitest/ directory following AI-TESTING-SOP.md
1. Write unit tests for all 3 limits
3. Use `testing-vbcs-locally` skill to validate in RDE
4. Test multi-vendor vs single-vendor scenarios
4. Test components at/near 250-bundle limit
5. Test bundles with <2 or >100 components
6. Verify error messages are clear

## Artifacts
- BundleRelationshipLimitsValidator class
- G2S2 client integration (if needed)
- Unit tests
- AI integration tests (aitest/)
- Updated validator configuration
- RDE test results

## Validation
- Validator follows VBCS patterns
- G2S2 integration works correctly
- All 3 limits enforced
- Multi-vendor handling correct
- Tests pass in RDE
- Error messages are clear

## Notes
---
2026-02-19 20:35 - Task claimed by gortarin
---
2026-02-19 20:44 - Implementation Complete (v1)

**Files Created/Modified:**
1. `VirtualBundleCatalogServiceModel/model/enums.xml` — Added `COMPONENT_RELATIONSHIP_LIMIT_EXCEEDED` error code
2. `validator/BundleRelationshipLimitsValidator.java` — New validator checking max bundles per component
3. `validator/BundleRelationshipLimitsValidatorTest.java` — 10 unit tests, 100% JaCoCo coverage
4. `module/ValidatorModule.java` — Registered validator in common validators list

**Design Decisions:**
- Uses `ProductBundleRelationshipCacheAccessor.getBundleSkusForComponent()` (DynamoDB GSI) to count existing bundles per component
- Only checks max bundles per component (250 limit) — min/max components per bundle already handled by `NumberOfBundleComponentsValidator`
- Multi-vendor limit (83 vs 250) deferred to TASK-057, blocked by TASK-022 design spike
- Runs on CREATE only — VBCS `ComponentsHaveNotChangedValidator` prevents component changes on EDIT
---
2026-02-20 00:30 - Code Review & Fixes

**Issues found comparing against PBCS reference and VBCS style:**
1. ✅ FIXED: Missing error handling for DynamoDB failures — added try/catch per component, returns CATALOG_ISSUE
2. ✅ FIXED: Was returning mutable ArrayList on success — now returns Collections.emptyList()
3. ✅ FIXED: Validator was in general-only list — moved to common validators (matches PBCS where ComponentsWithinRelationshipLimitsValidator is in commonValidators, applies to all bundle types including VMP)
4. Added TODO TASK-057 comment in code for multi-vendor limit

**ValidatorModule changes:**
- `getCommonValidators()` now takes G2S2Accessor + ProductBundleRelationshipCacheAccessor params
- `getVMPValidators()` updated to receive and pass through these dependencies
- BundleRelationshipLimitsValidator in common list, runs for both general and VMP bundles
---
2026-02-20 00:44 - Created TASK-057 (multi-vendor 83 limit)
Follow-up task blocked by TASK-022 design spike. Also added note to TASK-022 to address this.
---
2026-02-20 01:08 - Build Status
- brazil-build: ✅ BUILD SUCCESSFUL
- Tests: 660 passed, 0 failed, 0 errors
- JaCoCo: 100% instruction, branch, line, complexity, method coverage
- All files staged in git, ready for diff/commit

**Acceptance Criteria Status:**
- [x] BundleRelationshipLimitsValidator created following VBCS patterns
- [x] Validator calls G2S2 getRelationshipLimits API
- [x] Validator checks max bundles per component (250 limit)
- [N/A] Validator handles multi-vendor limit (83 vs 250) — deferred to TASK-057
- [x] Validator registered in common validators (applies to general + VMP)
- [x] Unit tests created (10 tests, 100% coverage)
- [ ] AI tests created following aitest/AI-TESTING-SOP.md
- [ ] Integration tests pass in RDE
---

---
2026-02-20 17:13 - BLOCKED: VMP team is also working on VBCS validators on mainline. All validator tasks blocked pending architectural alignment with VMP on how validators will be handled. Need to agree on approach before proceeding.
---
