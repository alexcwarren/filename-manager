import pathlib
import random
import sys

from _test_dir import _TestDir
from file_extensions import FILE_EXTENSIONS
import pytest

# Add project root and src to sys.path
project_root = pathlib.Path(__file__).resolve().parent.parent
src_path = project_root / "src"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--keep-test-dir", action="store_true")
    parser.addoption("--seed")


@pytest.fixture(autouse=True, scope="function")
def test_dir(request: pytest.FixtureRequest) -> pathlib.Path:
    seed: str = str(request.config.getoption("--seed")) or str(
        random.randrange(sys.maxsize)
    )
    testdir: _TestDir = _TestDir("./.test", seed=seed)

    keep_test_dir: bool = request.config.getoption("--keep-test-dir")
    if keep_test_dir:
        print(testdir)

    # Create nested function to call upon when pytest concludes
    def finalizer():
        if not keep_test_dir:
            testdir.cleanup()

    request.addfinalizer(finalizer)

    return testdir.path


@pytest.fixture(scope="session")
def file_extensions():
    return FILE_EXTENSIONS
