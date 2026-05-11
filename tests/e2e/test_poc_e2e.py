import pytest


pytestmark = pytest.mark.e2e


def test_api_create_user_ui_login_api_verify_session(user_service, login_page):
    user = user_service.create_user(email="poc-e2e@example.test", password="Password123!")
    try:
        login_page.open()
        login_page.login(user["email"], user["password"])

        session = user_service.create_session(user["email"], user["password"])
        user_service.verify_session(session["token"])
    finally:
        user_service.delete_user_by_email(user["email"])
