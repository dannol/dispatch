---
id: TASK-073
status: backlog
priority: high
created: 2026-02-24T18:10:00Z
updated: 2026-02-26T22:05:00Z
assignedTo: ""
dependencies: []
blockedBy: []
estimatedEffort: medium
tags: [design, spike, vbcs, deletion, mbws, migration, phase-2]
---

# TASK-073: Design Delete API and Bulk Delete Mechanism for VBCS

## Objective
Design the delete API and bulk delete mechanism for VBCS to replace the current MBWS-based deletion path.

## Context

### Decisions Already Made
- Migrate deletion from MBWS to VBCS (2026-02-12)
- VBCS already has CC `DeleteContribution` access — zero CloudAuth onboarding needed (ADR-017)

### Current PBXX Delete Flow
```
ABC → PBMS → SQS (per-SKU fan-out) → PBCW → MBWS (Coral) → CC DeleteContribution
```
5 hops across 4 services for what is ultimately a single CC API call. MBWS ended up here for historical/convenience reasons (intern project, MBWS already had CC access).

### Current VBCS State
- No DELETE workflow — `BundleOperation` enum only has CREATE and EDIT
- Stub exists: `SubmissionManager.deleteContribution()` returns null (TODO)
- CC client already configured with `TAAwareClientRequestFilter`

### Target
```
ABC → VBCS → CC DeleteContribution
```

### Protobuf model (current PBMS input, for reference)
```protobuf
message BulkDeleteContributionsRequest {
    repeated DeleteContributionRequest delete_contribution_request = 1;
}
message DeleteContributionRequest {
    optional int64 amazon_marketplace_id = 1;
    optional int64 merchant_customer_id = 2;
    optional string bundle_sku = 3;
    optional bool is_global_contribution = 4;
}
```

### TA Auth (detail, not a blocker)
PBCW currently self-issues a fresh TA token per delete via `CloudAuthTransitiveAuthTokenClient`. VBCS may be able to use `propagate=false` (service-to-service) instead — verify against CC behavior for existing CREATE/EDIT workflows. Implementation detail to resolve during design.

## Acceptance Criteria
- [ ] Delete API designed: `DeleteBundle` and `BulkDeleteBundles` operation signatures defined
- [ ] Bulk delete mechanism designed: fan-out strategy (ORCA workflow per SKU vs single workflow with loop)
- [ ] ORCA workflow activity sequence documented for `DeleteBundleWorkflow`
- [ ] TA auth approach documented in design: how VBCS handles (or avoids) TA tokens in ORCA async context, and proposed remediation — even if implementation tracked in TASK-072
- [ ] ABC migration path documented: changes to `BulkDeleteService` + `ProductBundleManagementServiceAdapter`
- [ ] ADR created for any new architectural decisions
- [ ] Design written to `/design` folder

## Implementation Guidance
1. Read any existing docs in `/design` folder and `design/MBWS-deprecation-design.md` first
2. Design the API contract (individual + bulk)
3. Design the ORCA workflow — activity sequence, inputs/outputs
4. Decide bulk fan-out strategy
5. Resolve TA auth as part of the design
6. Write it up, create ADR if needed

## Artifacts
- Created: design doc in `/design` folder
- Created: ADR if new architectural decisions made

## Notes
---
2026-02-26T17:31:00Z - Minimal DeleteBundle mirror API implementation split to TASK-078. This task retains scope for: bulk delete design, ORCA delete workflow, ABC migration path, TA auth for async context. TASK-078 can proceed independently without waiting on this design.

---
2026-02-26T21:49:00Z - THOROUGH VERIFICATION: Current delete contribution flow (PBMS source now available)

**Verified call chain from source code:**

1. `ProductBundleManagementController.bulkDeleteContributions()` (ABC) — Spring MVC entry point
2. `BulkDeleteService.deleteBundles()` (ABC) — builds `BulkDeleteContributionsRequest` proto
3. `ProductBundleManagementServiceAdapter.bulkDeleteContributions()` (ABC) — HTTP PUT to PBMS `/bundle/bulkDeleteBundles`
4. `DeleteContributionsController.bulkDeleteBundles()` (PBMS) — receives request, iterates per-SKU
5. `DeleteContributionsService.sendMessageDelete()` (PBMS) — encodes each `DeleteContributionRequest` as base64 protobuf, sends to SQS queue `bulk-delete-contributions-requests` (region-aware)
6. **SQS consumer: NOT identified in any locally available service.** PBCW only listens to `bulk-bundle-creation-requests` and `pba-contribution-catalog-updates`. MBWS has no SQS listener. No other worker service is checked out locally.
7. MBWS has two delete activities: `DeleteContributionsActivity` (direct Coral mirror) and `DeleteContributionsHerdActivity` (Herd SIL). The SQS consumer likely calls one of these — but the consumer service is not available locally to confirm.

**What is confirmed:**
- ABC → PBMS path: fully verified
- PBMS fans out per-SKU to SQS: fully verified (`DeleteContributionsService.sendMessageDelete()`)
- MBWS has CC delete capability: fully verified (`ContributionCatalogManager` → `ContributionCatalogAccessor` → CC `deleteContribution()` with TA token from PATI)
- PBCW is NOT the SQS consumer for delete: confirmed (only listens to creation and CC-updates queues)
- MBRS is NOT in the delete path: confirmed (`MarketplaceBundleWorkflowServiceAccessor` has no delete method)

**Unverified (consumer service not locally available):**
- What service consumes `bulk-delete-contributions-requests` SQS queue
- Whether it calls MBWS mirror (`DeleteContributionsActivity`) or Herd (`DeleteContributionsHerdActivity`)

**Best current understanding of flow:**
```
ABC → PBMS → SQS (bulk-delete-contributions-requests, per-SKU) → [unknown consumer] → MBWS → CC DeleteContribution
```

**Target flow:**
```
ABC → VBCS → CC DeleteContribution
```

---
2026-02-26T22:05:00Z - FULL FLOW VERIFIED: SQS consumer identified as PBCW (after pulling latest mainline)

**Complete verified call chain (all source-confirmed):**

1. `BulkDeleteService.bulkDelete()` (ABC) — parses form input, builds `BulkDeleteContributionsRequest` proto
2. `ProductBundleManagementServiceAdapter.bulkDeleteContributions()` (ABC) — HTTP PUT to PBMS `/bundle/bulkDeleteBundles`, propagates TA token via `TransitiveAuthPropagationStorage`
3. `DeleteContributionsController.bulkDeleteBundles()` (PBMS) — iterates per-SKU, calls `DeleteContributionsService.sendMessageDelete()` per SKU
4. `DeleteContributionsService.sendMessageDelete()` (PBMS) — base64-encodes each `DeleteContributionRequest` proto, publishes to SQS queue (`getContributionDeletionSqsQueue()`)
5. `ContributionDeletionSqsListener.processMessage()` (PBCW) — decodes protobuf, obfuscates merchant/marketplace IDs via `AmzUid.encryptCustomerID()`, calls `DeleteContributionsClient.deleteContribution()`
6. `DeleteContributionsClient.deleteContribution()` (PBCW) — calls `MarketplaceBundleWorkflowServiceClient.callDeleteContributions()` (Coral), propagates TA token via `TransitiveAuthPropagationStorage`
7. `DeleteContributionsActivity.enact()` (MBWS) — calls `ContributionCatalogManager.deleteBundle()`
8. `ContributionCatalogManager.deleteBundle()` (MBWS) — self-issues fresh TA token via PATI (`PartnerAuthorizationTokenIssuerAccessor.getTaToken()`), calls `ContributionCatalogAccessor.deleteContribution()`
9. `ContributionCatalogAccessor.deleteContribution()` (MBWS) — calls CC `deleteContribution()` REST endpoint with TA token; `propagate=true` for 3P, `propagate=false` for global/retail

**Fully verified flow:**
```
ABC → PBMS → SQS (per-SKU) → PBCW (ContributionDeletionSqsListener) → MBWS (DeleteContributionsActivity) → PATI → CC DeleteContribution
```

**Key design notes for VBCS migration:**
- PBCW uses a dedicated thread pool (`contributionDeletionSqsWorkerThreadPool`, sized by `numThreadsDelete`) for the delete listener — separate from creation
- MBWS ignores the propagated TA token from PBCW and self-issues a fresh one via PATI (`siteName=ccInternal`) — VBCS will need to do the same or verify service-to-service auth suffices
- CC `propagate` flag: `true` for 3P (marketplace-specific), `false` for global/retail contributions
- PBCW calls MBWS `DeleteContributions` (mirror/direct Coral), NOT `DeleteContributionsHerd`
