"""
Thin API client for the restful-booker service.

Wrapping the raw requests calls in one class keeps the tests declarative
("create a booking", "delete it") and puts URL/headers/auth concerns in a
single maintainable place -- the API equivalent of a Page Object.

Auth model (restful-booker):
  POST /auth {username, password} -> {"token": "..."}
  Mutating calls (PUT/DELETE) require   Cookie: token=<token>
"""

import requests

DEFAULT_TIMEOUT = 30  # seconds; the free Heroku dyno can be slow to wake


class BookingClient:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self._token = None

    # -- auth -------------------------------------------------------------
    def create_token(self, username=None, password=None):
        """POST /auth -> return the raw response (tests assert on it)."""
        payload = {
            "username": username if username is not None else self.username,
            "password": password if password is not None else self.password,
        }
        resp = requests.post(
            f"{self.base_url}/auth", json=payload, timeout=DEFAULT_TIMEOUT
        )
        # Cache a valid token so CRUD helpers can reuse it.
        if resp.ok and "token" in resp.json():
            self._token = resp.json()["token"]
        return resp

    def _auth_headers(self):
        if not self._token:
            self.create_token()
        return {"Cookie": f"token={self._token}"}

    # -- health -----------------------------------------------------------
    def ping(self):
        return requests.get(f"{self.base_url}/ping", timeout=DEFAULT_TIMEOUT)

    # -- CRUD -------------------------------------------------------------
    def create_booking(self, booking):
        return requests.post(
            f"{self.base_url}/booking", json=booking, timeout=DEFAULT_TIMEOUT
        )

    def get_booking(self, booking_id):
        return requests.get(
            f"{self.base_url}/booking/{booking_id}",
            headers={"Accept": "application/json"},
            timeout=DEFAULT_TIMEOUT,
        )

    def update_booking(self, booking_id, booking, headers=None):
        """PUT requires auth. Pass custom headers to test the unauthorized path."""
        send_headers = {"Accept": "application/json"}
        send_headers.update(self._auth_headers() if headers is None else headers)
        return requests.put(
            f"{self.base_url}/booking/{booking_id}",
            json=booking,
            headers=send_headers,
            timeout=DEFAULT_TIMEOUT,
        )

    def delete_booking(self, booking_id, headers=None):
        send_headers = self._auth_headers() if headers is None else headers
        return requests.delete(
            f"{self.base_url}/booking/{booking_id}",
            headers=send_headers,
            timeout=DEFAULT_TIMEOUT,
        )
