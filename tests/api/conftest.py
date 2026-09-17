"""API-layer fixtures."""

import pytest

from tests.api.booking_client import BookingClient


@pytest.fixture
def api(config):
    """A BookingClient pointed at the configured restful-booker instance."""
    return BookingClient(
        base_url=config["api_base_url"],
        username=config["api_username"],
        password=config["api_password"],
    )


@pytest.fixture
def sample_booking():
    """A valid booking payload used across create/update tests."""
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-05"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def created_booking(api, sample_booking):
    """
    Create a booking, hand its (id, body) to the test, then clean it up.

    Using a fixture for setup+teardown means every test starts from a known
    state and leaves no orphaned data behind -- proper test hygiene.
    """
    resp = api.create_booking(sample_booking)
    assert resp.status_code == 200, "Setup failed: could not create booking"
    booking_id = resp.json()["bookingid"]

    yield booking_id, sample_booking

    # Teardown: best-effort delete (ignore if the test already removed it).
    api.delete_booking(booking_id)
