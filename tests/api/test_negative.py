"""
Negative API tests: the system must reject bad input, not silently accept it.

These are the tests that show you think like a QA engineer, not just a
happy-path scripter.
"""

import allure
import pytest


@allure.feature("API: Auth boundaries")
@allure.story("Update without a token is forbidden")
@pytest.mark.negative
@pytest.mark.api
def test_update_without_token_returns_403(api, created_booking):
    booking_id, original = created_booking
    updated = dict(original, firstname="Hacker")

    # Send an explicitly tokenless header set -> should be rejected.
    resp = api.update_booking(booking_id, updated, headers={"Accept": "application/json"})
    assert resp.status_code == 403


@allure.feature("API: Auth boundaries")
@allure.story("Delete without a token is forbidden")
@pytest.mark.negative
@pytest.mark.api
def test_delete_without_token_returns_403(api, created_booking):
    booking_id, _ = created_booking
    resp = api.delete_booking(booking_id, headers={})
    assert resp.status_code == 403


@allure.feature("API: Data boundaries")
@allure.story("Fetching a non-existent booking returns 404")
@pytest.mark.negative
@pytest.mark.api
def test_get_missing_booking_returns_404(api):
    resp = api.get_booking(9999999)
    assert resp.status_code == 404


@allure.feature("API: Data boundaries")
@allure.story("Deleted booking is no longer retrievable")
@pytest.mark.negative
@pytest.mark.api
def test_get_deleted_booking_returns_404(api, sample_booking):
    booking_id = api.create_booking(sample_booking).json()["bookingid"]
    assert api.delete_booking(booking_id).status_code == 201

    # Reading it back must now fail.
    assert api.get_booking(booking_id).status_code == 404


@allure.feature("API: Data boundaries")
@allure.story("Creating a booking with missing required fields is rejected")
@pytest.mark.negative
@pytest.mark.api
def test_create_booking_with_missing_fields_is_rejected(api):
    """
    A payload missing required fields must not create a valid 200 booking.
    restful-booker responds 500 to a malformed body; the contract we assert
    is simply 'not a successful 200 create'.
    """
    resp = api.create_booking({"firstname": "OnlyName"})
    assert resp.status_code != 200, (
        f"Expected the malformed create to fail, got {resp.status_code}"
    )
