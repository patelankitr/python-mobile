import sys
# import os
# sys.path.insert(0, os.path.dirname(__file__))  # Add current directory to path
# import pytest_wrapper
import pytest
import allure
import datetime
import os
import shutil
import subprocess
from pathlib import Path
import pytest_asyncio

# Configure pytest-asyncio
def pytest_configure(config):
    config.option.asyncio_mode = "auto"

@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# @pytest_wrapper.hookimpl(hookwrapper=True)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # ✅ Create test name and timestamp
            test_name = item.name  # like test_verify_login_functionality
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_filename = f"{test_name}_{timestamp}.png"

            # ✅ Save screenshot
            screenshot = driver.get_screenshot_as_png()
            
            # ✅ Attach to Allure
            allure.attach(
                screenshot,
                name=screenshot_filename,
                attachment_type=allure.attachment_type.PNG
            )

SCREENSHOT_DIR = "screenshots"
RESULTS_DIR = "results"
def pytest_sessionstart(session):
    if os.path.exists(SCREENSHOT_DIR):
        shutil.rmtree(SCREENSHOT_DIR)
        print(f"🧹 Cleared existing screenshots in '{SCREENSHOT_DIR}'")
    if os.path.exists(RESULTS_DIR):
        shutil.rmtree(RESULTS_DIR)
        print(f"🧹 Cleared existing screenshots in '{RESULTS_DIR}'")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

def pytest_cmdline_main(config):
    """
    This hook is called *instead* of pytest's normal main entry
    if it returns a non-None integer. We use it to redirect
    -m smokey invocations into our runner.
    """
    
    if os.environ.get("PYTEST_RUNNER_ACTIVE") == "1":
        return None
    # 1) Only intercept when the marker expression includes "smokey"
    markexpr = getattr(config.option, "markexpr", "None")
    if not markexpr or "smokey" not in markexpr:
        return None   # let pytest do its normal thing

    # 2) Find the first .py file in config.args
    test_files = [arg for arg in config.args if Path(arg).suffix == ".py"]
    if not test_files:
        pytest.exit("❌ smokey mode requires you to pass at least one .py test file", 1)
    test_file = test_files[0]

    # 3) Build and call your runner script
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "run_tests.py"),
        "--test-file", test_file,
        # "-m", markexpr
    ]
    print(f"🔄 Detected smokey run; delegating to: {' '.join(cmd)}")
    
    # 🧠 Set env var to avoid recursive call
    env = os.environ.copy()
    env["PYTEST_RUNNER_ACTIVE"] = "1"

    rc = subprocess.call(cmd)

    # 4) Return its exit code to pytest so pytest will exit with the same status
    return rc
