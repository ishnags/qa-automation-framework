"""Auth + health tests for restful-booker."""

import allure
import pytest


@allure.feature("API: Health")
@allure.story("Service is up")
@pytest.mark.smoke
@pytest.mark.api
def test_ping_returns_201(api):
    """GET /ping is the service health check; it returns 201."""
    resp = api.ping()
    assert resp.status_code == 201


@allure.feature("API: Auth")
@allure.story("Obtain a token")
@pytest.mark.smoke
@pytest.mark.api
def test_create_token_with_valid_credentials(api):
    resp = api.create_token()
    assert resp.status_code == 200
    body = resp.json()
    assert "token" in body and body["token"], "Expected a non-empty token"


@allure.feature("API: Auth")
@allure.story("Reject bad credentials")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.api
def test_create_token_with_bad_credentials_has_no_token(api):
    """
    restful-booker returns 200 with {"reason": "Bad credentials"} instead of a
    token for invalid logins. The contract we assert is: no token is issued.
    """
    resp = api.create_token(username="nope", password="wrong")
    assert "token" not in resp.json()
    assert resp.json().get("reason") == "Bad credentials"
