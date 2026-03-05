import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--mode",
        action="store",
        default="all",
        choices=["ui", "api", "all"],
        help="ui, api"
    )
