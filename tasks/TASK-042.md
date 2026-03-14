---
id: TASK-042
status: backlog
priority: medium
created: 2026-02-12T21:32:00Z
updated: 2026-02-12T21:32:00Z
assignedTo: null
dependencies: [TASK-012]
blockedBy: []
estimatedEffort: small
tags: [workstream_implement, vbcs, attributes, implementation, phase-1]
skills: [writing-vbcs-code, analyzing-codebases, testing-vbcs-locally]
---

# TASK-042: Add rtip_product_line Attribute to VBCS

## Objective
Add rtip_product_line attribute to VBCS RollupAttributesManager.

## Context
TASK-012 (REQ-023) identified that VBCS is missing the rtip_product_line attribute. This should be set to "RTIP_BUNDLES" for retail bundles.

**VBCS Codebase:** `/Users/gortarin/workspace/VirtualBundleCatalogService`

## Acceptance Criteria
- [ ] rtip_product_line attribute added to RollupAttributesManager
- [ ] Set to "RTIP_BUNDLES" for retail bundles
- [ ] Unit tests created
- [ ] AI tests created following aitest/AI-TESTING-SOP.md
- [ ] Integration tests pass in RDE

## Implementation Guidance

### Phase 1: Setup and Study Patterns
1. Ensure working in pulse-ai branch: `git checkout pulse-ai`
2. Review RollupAttributesManager.java
3. Understand how to detect retail vs other bundle types

### Phase 2: Implement rtip_product_line
1. Add rtip_product_line attribute
2. Set to "RTIP_BUNDLES" for retail bundles
3. Handle non-retail bundles appropriately

### Phase 3: Testing
1. Write unit tests for retail and non-retail bundles
2. Create AI tests in aitest/ directory following AI-TESTING-SOP.md
3. Use `testing-vbcs-locally` skill to validate in RDE
4. Verify attribute appears correctly

## Artifacts
- Updated RollupAttributesManager.java
- Unit tests
- AI integration tests (aitest/)
- RDE test results

## Validation
- rtip_product_line set correctly for retail bundles
- Tests pass in RDE

## Notes
---
