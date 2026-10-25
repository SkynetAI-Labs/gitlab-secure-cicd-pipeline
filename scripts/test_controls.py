"""Prove scanners fail closed with ephemeral, synthetic fixtures; never log findings."""

import os
import secrets
import string
import subprocess
import tempfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory(prefix="release-gate-controls-") as temporary:
        root = Path(temporary)
        # A synthetic, randomly generated marker, never a valid account credential.
        marker = "ghp_" + "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(36)
        )
        (root / "fixture.txt").write_text(f'github_token = "{marker}"\n')
        scanner = os.environ.get("GITLEAKS_BIN", "gitleaks")
        result = subprocess.run(
            [scanner, "dir", "--redact", "--no-banner", str(root)],
            capture_output=True,
            timeout=60,
            check=False,
        )
        if result.returncode != 1:
            raise SystemExit("Secret detection control failed (expected finding exit code 1)")
        (root / "unsafe.py").write_text(
            "import subprocess\nsubprocess.run('echo test', shell=True)\n"
        )
        result = subprocess.run(
            ["bandit", "-q", "-r", str(root), "-f", "json"],
            capture_output=True,
            timeout=60,
            check=False,
        )
        if result.returncode != 1:
            raise SystemExit("Static-analysis control failed (expected finding exit code 1)")
    print("PASS: secret and unsafe-subprocess fixtures rejected; temporary fixtures removed")


if __name__ == "__main__":
    main()
