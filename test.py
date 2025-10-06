# python
import os
import sys
import subprocess
import difflib
from pathlib import Path

import pytest

# Import the function to test (absolute import). This satisfies the requirement.
from trucks import process_deliveries  # noqa: F401

BASE = Path(__file__).parent.resolve()

# Possible folder names (support both singular/plural as user may have either)
POSSIBLE_INPUT_DIRS = [BASE / "input", BASE / "inputs"]
POSSIBLE_OUTPUT_DIRS = [BASE / "output", BASE / "outputs"]

input_dir = next((d for d in POSSIBLE_INPUT_DIRS if d.exists()), None)
output_dir = next((d for d in POSSIBLE_OUTPUT_DIRS if d.exists()), None)

if input_dir is None or output_dir is None:
    pytest.skip(f"Could not find input/output directories. Checked: inputs {POSSIBLE_INPUT_DIRS}, outputs {POSSIBLE_OUTPUT_DIRS}")

# Gather test cases: pair an input file with expected output file of same name
input_files = sorted([p for p in input_dir.iterdir() if p.is_file()])
cases = []
for in_path in input_files:
    expected_path = output_dir / in_path.name
    if not expected_path.exists():
        pytest.fail(f"Expected output file not found for input {in_path.name}: looked for {expected_path}")
    cases.append((in_path, expected_path))

def _normalize_text(s: str) -> str:
    # Normalize CRLF, strip leading/trailing blank lines, and rstrip each line
    if s is None:
        return ""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = s.strip().split("\n")
    lines = [ln.rstrip() for ln in lines]
    return "\n".join(lines)

@pytest.mark.parametrize("input_path,expected_path", cases)
def test_program_against_expected_output(input_path: Path, expected_path: Path):
    env = os.environ.copy()
    # Prevent interactive plotting from blocking test runs
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("DISPLAY", "")
    # Run the main program as a script, using the project directory as working dir
    main_script = str(BASE / "main.py")
    with open(input_path, "rb") as fin:
        proc = subprocess.run(
            [sys.executable, main_script],
            stdin=fin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(BASE),
            env=env,
            timeout=15,
        )

    stdout = proc.stdout.decode("utf-8", errors="replace")
    stderr = proc.stderr.decode("utf-8", errors="replace")
    expected = expected_path.read_text(encoding="utf-8", errors="replace")

    actual_norm = _normalize_text(stdout)
    expected_norm = _normalize_text(expected)

    if actual_norm != expected_norm:
        # Build helpful diff
        diff = "\n".join(
            difflib.unified_diff(
                expected_norm.splitlines(),
                actual_norm.splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )
        msg = (
            f"Output mismatch for {input_path.name}\n"
            f"Return code: {proc.returncode}\n"
            f"Stdout:\n{stdout}\n"
            f"Stderr:\n{stderr}\n"
            f"Diff:\n{diff}"
        )
        pytest.fail(msg)