import json
import subprocess
import os
import sys
import platform
import psutil
import argparse
# import webbrowser


# Argument parser for dynamic test file path
parser = argparse.ArgumentParser(description="Run pytest with optional Allure reporting.")
parser.add_argument(
    "--test-file",
    type=str,
    required=True,
    help="Path to the test file to run (e.g., test/demo_simple_test/login/test_login.py)"
)
parser.add_argument(
    "-m", "--marker",
    type=str,
    required=False,
    help="Pytest marker to filter tests (e.g., smokey, regression)"
)
args = parser.parse_args()
TEST_FILE = args.test_file
MARKER = args.marker
CONFIG_PATH = "config/TestConfig.json"
RESULTS_DIR = "results"
REPORT_DIR = "reports/allure"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Config file '{CONFIG_PATH}' not found.")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)

def run_tests(use_allure: bool):
    print("📦 Running tests...")
    print(f"✅ TEST_FILE: {TEST_FILE}")
    cmd = ["pytest", TEST_FILE]
    if MARKER:
        print(f"✅ Using marker: {MARKER}")
        cmd = ["pytest", "-m", MARKER, TEST_FILE]
    if use_allure:
        print(f"✅ RESULTS_DIR: {RESULTS_DIR}")
        cmd += ["--alluredir", RESULTS_DIR]
    print(f"✅ Allure cmd: {cmd}")
    subprocess.run(cmd)

def detect_terminal():
    # On Windows, COMSPEC is usually set
    comspec = os.environ.get("COMSPEC", "").lower()
    shell = os.environ.get("SHELL", "").lower()

    # Use psutil to trace the parent process
    parent_name = ""
    try:
        parent = psutil.Process().parent()
        parent_name = parent.name().lower()
    except Exception:
        pass

    if "cmd.exe" in comspec or "cmd" in parent_name:
        return "cmd"
    elif "powershell.exe" in comspec or "powershell" in parent_name:
        return "powershell"
    elif "bash" in shell or "git" in parent_name:
        return "bash"
    elif platform.system() == "Darwin":
        return "macos"
    elif "linux" in platform.system().lower():
        return "linux"
    
    return "unknown"

def get_allure_path():
    terminal = detect_terminal()
    
    if terminal == "cmd":
        cmd = ["where", "allure"]
    elif terminal == "powershell":
        cmd = ["powershell", "-Command", "Get-Command allure | Select-Object -ExpandProperty Source"]
    elif terminal in ("bash", "linux", "macos"):
        cmd = ["which", "allure"]
    else:
        print("Unknown terminal environment. Defaulting to 'which'.")
        cmd = ["which", "allure"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        path = result.stdout.strip()

        # Filter for the .bat path (or use the last line as fallback)
        lines = path.splitlines()
        bat_path = next((line for line in lines if line.lower().endswith(".bat")), lines[-1])

        print(f"[{terminal.upper()}] Allure path: {bat_path}")
        return bat_path

    except subprocess.CalledProcessError as e:
        print(f"Failed to locate Allure in {terminal.upper()} terminal.")
        print("Error:", e.stderr or e.stdout)
        return None

def generate_allure_report():
    print("📊 Generating Allure report...")
    # Define your command as a list of arguments
    allure_path = get_allure_path()
    print(f"✅ terminal: {allure_path}")


    command = [
        allure_path,
        "generate",
        RESULTS_DIR,
        "-o",
        REPORT_DIR,
        "--clean"
    ]
    # Run the command
    subprocess.run(command, check=True)

    # subprocess.run(["allure", "generate", RESULTS_DIR, "-o", REPORT_DIR, "--clean"])

def main():
    config = load_config()
    use_allure = config["config"].get("report", False)
    print(f"✅ use_allure: {use_allure}")
    run_tests(use_allure)

    if use_allure:
        generate_allure_report()
        print(f"✅ Allure report generated at: http://127.0.0.1:5500/reports/allure/index.html")
        #webbrowser.open(f"{REPORT_DIR}/index.html")

if __name__ == "__main__":
    main()
