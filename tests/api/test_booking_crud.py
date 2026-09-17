"""Full CRUD lifecycle for a booking: create -> read -> update -> delete."""

import allure
import pytest


@allure.feature("API: Booking CRUD")
@allure.story("Create a booking")
@pytest.mark.functional
@pytest.mark.api
def test_create_booking(api, sample_booking):
    resp = api.create_booking(sample_booking)
    assert resp.status_code == 200
    body = resp.json()
    assert "bookingid" in body
    assert body["booking"]["firstname"] == sample_booking["firstname"]

    # Clean up what this test created.
    api.delete_booking(body["bookingid"])


@allure.feature("API: Booking CRUD")
@allure.story("Read a booking")
@pytest.mark.functional
@pytest.mark.api
def test_get_booking(api, created_booking):
    booking_id, expected = created_booking
    resp = api.get_booking(booking_id)
    assert resp.status_code == 200
    assert resp.json()["firstname"] == expected["firstname"]
    assert resp.json()["lastname"] == expected["lastname"]


@allure.feature("API: Booking CRUD")
@allure.story("Update a booking (requires auth)")
@pytest.mark.regression
@pytest.mark.api
def test_update_booking(api, created_booking):
    booking_id, original = created_booking
    updated = dict(original, firstname="Jane", totalprice=250)

    resp = api.update_booking(booking_id, updated)
    assert resp.status_code == 200
    assert resp.json()["firstname"] == "Jane"
    assert resp.json()["totalprice"] == 250


@allure.feature("API: Booking CRUD")
@allure.story("Delete a booking")
@pytest.mark.regression
@pytest.mark.api
def test_delete_booking(api, sample_booking):
    booking_id = api.create_booking(sample_booking).json()["bookingid"]

    resp = api.delete_booking(booking_id)
    # restful-booker returns 201 on a successful DELETE.
    assert resp.status_code == 201

    # And the booking is really gone.
    assert api.get_booking(booking_id).status_code == 404
