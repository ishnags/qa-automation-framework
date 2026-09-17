# Defect Log — QA Automation Framework

Severity scale: **S1 Critical** (blocks core flow / data loss) · **S2 Major**
(feature broken, workaround exists) · **S3 Minor** (cosmetic / edge) ·
**S4 Trivial**.
Status: **Open · In Progress · Fixed · Won't Fix · Closed**.

> These defects were surfaced by the automated suite against the demo AUTs.
> SauceDemo intentionally ships some "planted" bugs behind specific users
> (`problem_user`, `performance_glitch_user`) — a realistic hunting ground for
> writing defect reports. Reproduce and confirm each before your interview so
> you can speak to it firsthand, then update Status.

---

| ID | Title | Env / User | Steps to Reproduce | Expected | Actual | Severity | Status | Found by |
|----|-------|-----------|--------------------|----------|--------|----------|--------|----------|
| DEF-01 | Locked-out user can reach login submit but is blocked with unclear recovery path | SauceDemo / locked_out_user | 1. Open site 2. Login as `locked_out_user` / `secret_sauce` | Clear error + guidance | Error shown but no unlock/contact path | S3 Minor | Open | TC-UI-05 |
| DEF-02 | `problem_user` product images are all identical (wrong image mapping) | SauceDemo / problem_user | 1. Login as `problem_user` 2. View inventory | Each product shows its own image | All items show the same dog image | S2 Major | Confirmed | `scripts/verify_defects.py` |
| DEF-03 | `problem_user` sort dropdown does not reorder products | SauceDemo / problem_user | 1. Login as `problem_user` 2. Select "Name (Z to A)" | List reorders Z→A | Order does not change | S2 Major | Confirmed | `scripts/verify_defects.py` |
| DEF-04 | `performance_glitch_user` login is abnormally slow | SauceDemo / performance_glitch_user | 1. Login as `performance_glitch_user` | Inventory loads promptly | Multi-second delay before inventory | S3 Minor | Open | TC-UI-04 |
| DEF-05 | restful-booker returns HTTP 500 (not 400) for malformed create payload | restful-booker | 1. POST /booking with only `firstname` | 400 Bad Request | 500 Internal Server Error | S3 Minor | Open | TC-API-12 |
| DEF-06 | restful-booker `/auth` returns 200 with "Bad credentials" instead of 401 | restful-booker | 1. POST /auth with wrong creds | 401 Unauthorized | 200 + `{"reason":"Bad credentials"}` | S3 Minor | Open | TC-API-03 |

---

## Verification evidence

DEF-02 and DEF-03 were reproduced programmatically via `scripts/verify_defects.py`
(logs in as `problem_user`):

```
DEF-02 (identical product images): CONFIRMED -> 6 images, 1 unique
DEF-03 (sort dropdown does nothing): CONFIRMED -> after-sort order unchanged, matches expected Z->A: False
```

## Notes on writing good defect reports (for the interview)

- **Severity vs Priority:** severity = impact on the system; priority = urgency
  to fix. DEF-02 is S2 (feature clearly broken) but a demo site would fix it at
  low priority.
- **Reproducibility matters:** every row has exact steps + the user account,
  because a defect a dev can't reproduce won't get fixed.
- **Expected vs Actual with evidence:** in a real report, attach the Allure
  screenshot (the framework auto-captures one on UI failure).
