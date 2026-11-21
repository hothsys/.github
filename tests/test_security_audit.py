"""Exercise the actual inline scan step without network access or GitHub writes."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/reusable-security-audit.yml"


def scan_script():
    text = WORKFLOW.read_text()
    block = text.split("      - name: Scan for known vulnerabilities\n", 1)[1]
    block = block.split("        run: |\n", 1)[1].split("\n      - name:", 1)[0]
    return "\n".join(line[10:] for line in block.splitlines())


class ScanOutcomes(unittest.TestCase):
    def run_scan(self, code):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scanner = root / "osv-scanner"
            scanner.write_text(f"#!/bin/bash\nexit {code}\n")
            scanner.chmod(0o755)
            output = root / "output"
            summary = root / "summary"
            script = scan_script().replace("/tmp/", f"{root}/")
            result = subprocess.run(
                ["bash", "-e", "-o", "pipefail", "-c", script],
                env={
                    **os.environ,
                    "GITHUB_OUTPUT": str(output),
                    "GITHUB_STEP_SUMMARY": str(summary),
                },
                capture_output=True,
                text=True,
                check=False,
            )
            return (
                result,
                output.read_text() if output.exists() else "",
                summary.read_text() if summary.exists() else "",
            )

    def test_clean(self):
        result, output, summary = self.run_scan(0)
        self.assertEqual(result.returncode, 0)
        self.assertIn("status=clean\n", output)
        self.assertIn("found=false\n", output)
        self.assertIn("Result: clean", summary)

    def test_findings(self):
        result, output, _ = self.run_scan(1)
        self.assertEqual(result.returncode, 0)
        self.assertIn("status=findings\n", output)
        self.assertIn("found=true\n", output)

    def test_no_packages_is_not_clean(self):
        result, output, summary = self.run_scan(128)
        self.assertEqual(result.returncode, 0)
        self.assertIn("status=not-applicable\n", output)
        self.assertIn("found=unknown\n", output)
        self.assertNotIn("found=false", output)
        self.assertIn("not a clean security scan", summary)
        self.assertIn("left open", summary)

    def test_other_errors_fail_closed(self):
        for code in (2, 126, 127, 129, 130):
            with self.subTest(code=code):
                result, output, _ = self.run_scan(code)
                self.assertEqual(result.returncode, code)
                self.assertEqual(output, "")

    def test_issue_steps_require_the_exact_status(self):
        text = WORKFLOW.read_text()
        report = text.split("      - name: Report findings as an issue\n", 1)[1]
        close = text.split("      - name: Close audit issue when clean\n", 1)[1]
        self.assertIn("if: steps.scan.outputs.status == 'findings'", report.split("env:", 1)[0])
        self.assertIn("if: steps.scan.outputs.status == 'clean'", close.split("env:", 1)[0])


if __name__ == "__main__":
    unittest.main()
