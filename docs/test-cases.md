# Test Cases — QA Automation Framework

Legend: **P** = Pass, **F** = Fail, **N/A** = not run.
Each case maps to an automated test; the "Automated by" column points to it.

---

## UI — Authentication

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-UI-01 | Login page loads | App reachable | Open base URL | Login logo + username/password fields visible | High | Smoke | P | `test_login.py::test_login_page_loads` |
| TC-UI-02 | Valid login (standard_user) | On login page | Enter valid creds, submit | Redirected to inventory page | High | Smoke | P | `test_login.py::test_valid_login` |
| TC-UI-03 | Valid login (problem_user) | On login page | Enter valid creds, submit | Reaches inventory page | Medium | Smoke | P | `test_login.py::test_valid_login` |
| TC-UI-04 | Valid login (performance_glitch_user) | On login page | Enter valid creds, submit | Reaches inventory page (may be slow) | Medium | Smoke | P | `test_login.py::test_valid_login` |
| TC-UI-05 | Locked-out user rejected | On login page | Login as locked_out_user | Error: "Sorry, this user has been locked out." | High | Regression/Negative | P | `test_login.py::test_invalid_login_is_rejected` |
| TC-UI-06 | Wrong password rejected | On login page | Valid user + wrong password | Error: credentials do not match | High | Regression/Negative | P | `test_login.py::test_invalid_login_is_rejected` |
| TC-UI-07 | Empty username rejected | On login page | Blank username, submit | Error: "Username is required" | Medium | Regression/Negative | P | `test_login.py::test_invalid_login_is_rejected` |
| TC-UI-08 | Empty password rejected | On login page | Blank password, submit | Error: "Password is required" | Medium | Regression/Negative | P | `test_login.py::test_invalid_login_is_rejected` |

## UI — Cart

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-UI-09 | Add single item updates badge | Logged in | Add backpack | Cart badge shows 1 | High | Functional | P | `test_cart.py::test_add_item_updates_cart_count` |
| TC-UI-10 | Add multiple items | Logged in | Add 3 items | Cart badge shows 3 | Medium | Functional | P | `test_cart.py::test_add_multiple_items` |
| TC-UI-11 | Item appears on cart page | Logged in, item added | Open cart | Cart lists the added item | High | Regression | P | `test_cart.py::test_item_appears_on_cart_page` |

## UI — Checkout

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-UI-12 | Complete order (data-driven ×3) | Logged in | Add item → cart → checkout → fill info → finish | "Thank you for your order!" shown | High | Functional | P | `test_checkout.py::test_complete_checkout` |
| TC-UI-13 | Missing first name rejected | In checkout step one | Leave first name blank, continue | Error: "First Name is required" | High | Regression/Negative | P | `test_checkout.py::test_checkout_missing_first_name_is_rejected` |

## UI — Inventory sorting

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-UI-14 | Sort Name A→Z | Logged in | Select "Name (A to Z)" | Products in ascending order | Medium | Regression | P | `test_sorting.py::test_sort_name_a_to_z` |
| TC-UI-15 | Sort Name Z→A | Logged in | Select "Name (Z to A)" | Products in descending order | Medium | Regression | P | `test_sorting.py::test_sort_name_z_to_a` |

## API — Auth & Health

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-API-01 | Health check | Service reachable | GET /ping | 201 | High | Smoke | P | `test_auth.py::test_ping_returns_201` |
| TC-API-02 | Create token (valid) | — | POST /auth valid creds | 200 + non-empty token | High | Smoke | P | `test_auth.py::test_create_token_with_valid_credentials` |
| TC-API-03 | Bad credentials issue no token | — | POST /auth bad creds | Body has "Bad credentials", no token | Medium | Regression/Negative | P | `test_auth.py::test_create_token_with_bad_credentials_has_no_token` |

## API — Booking CRUD

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-API-04 | Create booking | — | POST /booking valid payload | 200 + bookingid returned | High | Functional | P | `test_booking_crud.py::test_create_booking` |
| TC-API-05 | Read booking | Booking exists | GET /booking/{id} | 200 + matching data | High | Functional | P | `test_booking_crud.py::test_get_booking` |
| TC-API-06 | Update booking (auth) | Booking exists, token held | PUT /booking/{id} | 200 + updated fields | High | Regression | P | `test_booking_crud.py::test_update_booking` |
| TC-API-07 | Delete booking | Booking exists, token held | DELETE /booking/{id} | 201; subsequent GET → 404 | High | Regression | P | `test_booking_crud.py::test_delete_booking` |

## API — Negative / Boundaries

| ID | Title | Preconditions | Steps | Expected Result | Priority | Type | Status | Automated by |
|----|-------|---------------|-------|-----------------|----------|------|--------|--------------|
| TC-API-08 | Update without token forbidden | Booking exists | PUT without Cookie token | 403 | High | Negative | P | `test_negative.py::test_update_without_token_returns_403` |
| TC-API-09 | Delete without token forbidden | Booking exists | DELETE without token | 403 | High | Negative | P | `test_negative.py::test_delete_without_token_returns_403` |
| TC-API-10 | Missing booking returns 404 | — | GET /booking/9999999 | 404 | Medium | Negative | P | `test_negative.py::test_get_missing_booking_returns_404` |
| TC-API-11 | Deleted booking not retrievable | Booking created+deleted | GET /booking/{id} | 404 | Medium | Negative | P | `test_negative.py::test_get_deleted_booking_returns_404` |
| TC-API-12 | Malformed create rejected | — | POST /booking missing fields | Not 200 (rejected) | Medium | Negative | P | `test_negative.py::test_create_booking_with_missing_fields_is_rejected` |

## BDD (Gherkin) — Login

| ID | Title | Scenario | Expected Result | Status | Automated by |
|----|-------|----------|-----------------|--------|--------------|
| TC-BDD-01 | Successful login | valid creds | Products page shown | P | `login.feature` |
| TC-BDD-02 | Locked-out rejected | locked_out_user | Locked-out error | P | `login.feature` |
| TC-BDD-03 | Wrong password rejected | bad password | Credential-mismatch error | P | `login.feature` |

---

**Totals:** 15 UI + 12 API + 3 BDD case IDs (parametrization expands several,
e.g. TC-UI-02..04, TC-UI-12 ×3, into more executed instances).
Fill in the Status column with real results after your first full run.
