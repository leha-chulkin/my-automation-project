import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.helpers import pytest_addoption

def run_tests(mode="all"):
    args = []
    if mode == "ui":
        args.append("tests/test_ui.py")
    elif mode == "api":
        args.append("tests/test_api.py")
    else:
        args.append("tests/")

    pytest_args = args
    pytest.main(pytest_args)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        run_tests(mode)
    else:
        run_tests()
