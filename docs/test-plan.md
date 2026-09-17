# Test Plan — QA Automation Framework

**Document version:** 1.0
**Author:** Ishna S
**Applications under test:**
- **UI:** Swag Labs / SauceDemo — `https://www.saucedemo.com`
- **API:** restful-booker — `https://restful-booker.herokuapp.com`

---

## 1. Introduction & Objective

This plan describes the test strategy for an automated regression framework that
validates a web storefront (UI) and a booking REST API. The objective is to
provide fast, repeatable, CI-integrated verification of core user journeys and
API contracts, with professional reporting and documentation that follows the
Software Testing Life Cycle (STLC).

## 2. Scope

### 2.1 In scope
| Area | Coverage |
|------|----------|
| Authentication (UI) | Valid login, locked-out user, wrong password, empty fields |
| Cart (UI) | Add single/multiple items, cart badge count, cart page contents |
| Checkout (UI) | Full happy-path order, missing-field validation |
| Inventory (UI) | Product sorting (A→Z, Z→A) |
| Auth (API) | Health check (`/ping`), token generation, bad-credential handling |
| Booking CRUD (API) | Create, read, update (authorized), delete |
| API negatives | 403 without token, 404 for missing/deleted booking, malformed create |

### 2.2 Out of scope
- Payment gateway / real transactions (SauceDemo is a mock store)
- Performance / load testing
- Security / penetration testing
- Visual pixel-level regression
- Mobile-native apps

## 3. Test Approach

- **Design pattern:** Page Object Model (POM). Each page's locators and actions
  live in one class under `pages/`; tests read as user journeys, not selectors.
- **Levels:** Smoke → Functional → Regression, sliced by pytest markers.
- **Data-driven:** Login cases come from `data/login_data.json`; checkout data
  from `data/checkout_data.csv`. New cases are data edits, not code changes.
- **BDD:** The login flow is additionally expressed in Gherkin
  (`tests/features/login.feature`) via pytest-bdd to document behaviour in
  business-readable Given/When/Then.
- **API testing:** A `BookingClient` wraps `requests` (the API analogue of a
  Page Object) so tests stay declarative.

## 4. Test Environment & Tools

| Concern | Tool |
|---------|------|
| Language | Python 3.11 |
| UI automation | Selenium WebDriver 4 |
| Test runner | pytest |
| API client | requests |
| BDD | pytest-bdd (Gherkin) |
| Parallel execution | pytest-xdist |
| Cross-browser infra | Selenium Grid (Docker: Chrome + Firefox nodes) |
| Containerization | Docker + docker-compose |
| Reporting | Allure (primary), pytest-html (fallback) |
| CI/CD | GitHub Actions |
| Flaky mitigation | Explicit waits (WebDriverWait) + pytest-rerunfailures |

## 5. Entry & Exit Criteria

**Entry:** AUT reachable; dependencies installed; test data available.
**Exit:** All smoke tests pass; ≥95% of regression tests pass; every failure is
triaged and logged in `defect-log.md`; Allure report generated.

## 6. Flaky-Test Strategy (design rationale)

Flakiness is treated as a first-class concern (and ties into the companion
FlakeFlagger analysis project):

1. **Explicit waits, never `time.sleep()`.** `BasePage` uses `WebDriverWait`
   with `expected_conditions` (visibility / clickability). This waits exactly as
   long as needed and no longer, eliminating the timing races that cause the
   most common Selenium flakiness.
2. **Function-scoped driver.** Every test gets a fresh, isolated browser, so no
   state leaks between tests.
3. **Fixture-based setup/teardown.** API bookings are created and deleted per
   test, guaranteeing a known starting state.
4. **Controlled retry.** `pytest-rerunfailures` can re-run a genuinely flaky
   test (`--reruns 2`) to distinguish infrastructure blips from real defects —
   used deliberately, not to paper over bugs.

## 7. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| restful-booker free dyno sleeps / is slow | 30s request timeout; `/ping` warm-up |
| Public demo data changes | SauceDemo is intentionally stable; API data created per test |
| Browser/driver version drift | Selenium Manager (local) + pinned Grid image tags (CI) |
| Network flakiness in CI | Explicit waits + bounded reruns |

## 8. Deliverables

- Automated suite (UI + API + BDD)
- `docs/test-cases.md` — test case catalogue
- `docs/defect-log.md` — severity-rated defect log
- Allure execution report (CI artifact)
