"""safety dynamic pytest wrapper"""

import glob
import subprocess
import json
import pytest

# List of CVEs to ignore
IGNORED_CVES = [
    'CVE-2024-34064',
    'CVE-2019-8341',
    'CVE-2024-35195',  # Example: Jinja CVE
    # Add more CVEs here if necessary
]

FILTER = './../../**/requirements.txt'
PYTHON_FILES = glob.glob(FILTER, recursive=True)


@pytest.mark.parametrize('filepath', PYTHON_FILES)
def test_file_has_no_safety_errors(filepath):
    """validate that there are zero safety warnings against a python file"""
    print(F"creating tests for file {filepath}")

    with subprocess.Popen("safety check --file=" + filepath + " --json",
                          stdout=subprocess.PIPE, shell=True) as proc:
        (out, _err) = proc.communicate()

    lint_json = []
    if out and out.strip():
        lint_json = json.loads(out)
        print(out)

        # Filter out ignored vulnerabilities
        filtered_vulnerabilities = [
            vuln for vuln in lint_json['vulnerabilities'] if vuln['CVE'] not in IGNORED_CVES  # noqa: E501
        ]

        # Assert that there are no unignored vulnerabilities
        assert len(filtered_vulnerabilities) == 0, F"Found vulnerabilities: {filtered_vulnerabilities}"  # noqa: E501
