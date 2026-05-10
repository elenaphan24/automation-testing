import pytest


pytestmark = pytest.mark.ui


def test_login_page_poc(login_page):
    login_page.open()
    login_page.assert_title_contains("Sandbox")
    login_page.screenshot("login-page-poc")

