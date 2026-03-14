---
id: TASK-058
status: backlog
priority: medium
created: 2026-02-20T01:10:47Z
updated: 2026-02-20T01:10:47Z
assignedTo: gortarin
dependencies: []
blockedBy: []
estimatedEffort: medium
tags: [workstream_test, testing, vbcs, test-data, infrastructure]
---

# TASK-058: Build VBCS Test Account Portfolio

## Objective
Populate the test data registry with a comprehensive portfolio of test accounts and ASINs for VBCS testing across different scenarios.

## Context
TASK-033 created the test data management infrastructure (vbcs-manage-test-data skill and test-data-registry.json). Now we need to build out the actual portfolio of test accounts and ASINs that can be used for various VBCS testing scenarios.

Work completed so far:
- Created test-data-registry.json schema
- Created vbcs-manage-test-data skill for managing accounts/ASINs
- Added seller account A3SNCN62TATVPA with component ASINs for attribute rollup testing
- Documented attribute rollup test data with sample payload

## Acceptance Criteria
- [ ] Registry contains at least 5 different test accounts (mix of vendor and seller)
- [ ] Each account has associated component ASINs documented
- [ ] Coverage for both beta and prod environments
- [ ] Coverage for both standard and VMP test types
- [ ] Test accounts cover key testing scenarios (attribute rollup, pricing models, multi-component bundles)
- [ ] Each account documents what it can be used for (capabilities, test scenarios)
- [ ] Registry is synced to repo for team access

## Implementation Guidance

1. Identify test accounts from existing VBCS testing:
   - Review integration test code for existing test accounts
   - Check with team for known test accounts
   - Document marketplace, environment, capabilities

2. For each account, gather:
   - MCID or Vendor Code
   - Account type (vendor/seller)
   - Marketplace
   - Environment (beta/prod)
   - Usable in (sandbox/pipeline)
   - Test type (standard/vmp)
   - Capabilities (canCreateBundles, deleteAfterTest)
   - Component ASINs with details

3. Add accounts to registry using vbcs-manage-test-data skill operations

4. Document test scenarios for each account:
   - What can be tested with this account
   - Sample payloads if available
   - Known limitations

5. Sync to repo for team access

## Artifacts
- `project/testing/test-data-registry.json` - Updated with new accounts/ASINs
- `project/testing/test-scenarios/` - Directory with scenario documentation per account
- Updated TASK-058.md with progress notes

## Validation
- Registry contains at least 5 accounts with full metadata
- Each account has at least 2 component ASINs
- Test scenarios documented for each account
- Registry synced to mainline branch
- Team can access and use the registry

## Notes
---
2026-02-20T01:10:47Z - Task created, split from TASK-033 to focus on building test data portfolio

2026-02-20T01:47:23Z - Progress: Added vendor account (AmazonUs/BUNDX, MCID 410611560) and product_bundle test data (BT6TLYSJJK + components) to registry. Found VBCS integration test accounts in TestDataHelper.java. Closed TASK-051 as duplicate.

## Open Issues

### ISSUE-1: MCID for cascade-dev+NABundles account unknown
- **Account**: cascade-dev+NABundles@amazon.com (old 3P test account, beta)
- **Problem**: Don't have the MCID or obfuscated merchant customer ID
- **Source**: Sajid mentioned in #bb-conclave on 2026-01-21
- **Action needed**: Look up in Merchant Portal or ask Sajid
- **Wiki search blocked** (403), wiki page also 403: `CETech/TeamMTN/BasketBuilding/Bundles/Operations/Runbook/3P/ProdMerchantBundleCreation`

### ISSUE-2: Two different MCIDs for pba-dev+brandOwner account
- **Registry has**: A3SNCN62TATVPA (merchant 558205166807)
- **Integration tests use**: A1R35UEB5FE7F5 (also labeled pba-dev+brandOwner@amazon.com)
- **Problem**: Are these the same account with different MCIDs (e.g., different marketplaces)? Or two different accounts?
- **Action needed**: Clarify relationship, update registry accordingly

### ISSUE-3: Wiki access blocked for test account documentation
- **Blocked wikis**:
  - `Users/qwlou/VendorCentralBundleManagement/Development` (vendor test accounts from former dev)
  - `CETech/TeamMTN/BasketBuilding/Bundles/Operations/Runbook/3P/ProdMerchantBundleCreation` (3P test account setup)
- **Problem**: 403 on both read and search — can't extract vendor group links or test account details
- **Action needed**: Get wiki access or have someone with access extract the test account info

### ISSUE-4: No prod test accounts identified yet
- **Problem**: All accounts found so far are beta. Need prod coverage for TASK-058 acceptance criteria.
- **Action needed**: Identify or create prod test accounts (seller and vendor)
