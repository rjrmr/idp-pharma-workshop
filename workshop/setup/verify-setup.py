#!/usr/bin/env python3
"""
Pre-flight verification script for the IDP Pharma Workshop.

Checks that the workshop environment is properly configured:
- Python dependencies importable (strands_agents, streamlit, boto3)
- AWS credentials configured
- MCP server configuration exists and is valid JSON

Usage:
    python workshop/setup/verify-setup.py

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import json
import os
import sys


class CheckResult:
    """Result of a single pre-flight check."""

    def __init__(self, component, status, message, remediation=None):
        self.component = component
        self.status = status  # "PASS" or "FAIL"
        self.message = message
        self.remediation = remediation


def check_python_dependency(module_name, display_name):
    """Check if a Python module is importable."""
    try:
        __import__(module_name)
        return CheckResult(
            component=f"Python: {display_name}",
            status="PASS",
            message=f"{module_name} module is importable",
        )
    except ImportError:
        return CheckResult(
            component=f"Python: {display_name}",
            status="FAIL",
            message=f"Could not import {module_name} module",
            remediation="Run 'pip install -r workshop/setup/requirements.txt'",
        )


def check_aws_credentials():
    """Check if AWS credentials are configured via boto3."""
    try:
        import boto3

        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is not None:
            return CheckResult(
                component="AWS Credentials",
                status="PASS",
                message="AWS credentials are configured",
            )
        else:
            return CheckResult(
                component="AWS Credentials",
                status="FAIL",
                message="No AWS credentials found",
                remediation=(
                    "Run 'aws configure' or set AWS_ACCESS_KEY_ID and "
                    "AWS_SECRET_ACCESS_KEY environment variables"
                ),
            )
    except ImportError:
        return CheckResult(
            component="AWS Credentials",
            status="FAIL",
            message="Cannot check AWS credentials (boto3 not installed)",
            remediation="Run 'pip install -r workshop/setup/requirements.txt'",
        )
    except Exception as e:
        return CheckResult(
            component="AWS Credentials",
            status="FAIL",
            message=f"Error checking AWS credentials: {e}",
            remediation=(
                "Run 'aws configure' or set AWS_ACCESS_KEY_ID and "
                "AWS_SECRET_ACCESS_KEY environment variables"
            ),
        )


def check_mcp_config():
    """Check that MCP server configuration exists and is valid JSON."""
    config_path = os.path.join("workshop", "setup", "mcp-config.json")

    if not os.path.isfile(config_path):
        return CheckResult(
            component="MCP Configuration",
            status="FAIL",
            message=f"MCP config file not found at {config_path}",
            remediation=(
                "Ensure workshop/setup/mcp-config.json exists. "
                "Copy from the template and fill in your AWS_REGION and BDA_PROJECT_ARN values."
            ),
        )

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return CheckResult(
            component="MCP Configuration",
            status="FAIL",
            message=f"MCP config file contains invalid JSON: {e}",
            remediation=(
                "Fix the JSON syntax in workshop/setup/mcp-config.json. "
                "Ensure it is valid JSON with proper formatting."
            ),
        )

    # Validate expected structure: must have mcpServers with at least one server entry
    if "mcpServers" not in config:
        return CheckResult(
            component="MCP Configuration",
            status="FAIL",
            message="MCP config missing 'mcpServers' key",
            remediation=(
                "Ensure workshop/setup/mcp-config.json contains a 'mcpServers' object "
                "with at least one server configuration (e.g., 'bda')."
            ),
        )

    if not isinstance(config["mcpServers"], dict) or len(config["mcpServers"]) == 0:
        return CheckResult(
            component="MCP Configuration",
            status="FAIL",
            message="MCP config 'mcpServers' is empty or not an object",
            remediation=(
                "Add at least one MCP server entry under 'mcpServers' in "
                "workshop/setup/mcp-config.json (e.g., 'bda' server configuration)."
            ),
        )

    return CheckResult(
        component="MCP Configuration",
        status="PASS",
        message="MCP config file found and valid",
    )


def print_results(results):
    """Print formatted pre-flight check results."""
    print()
    print("Pre-flight Environment Check")
    print("============================")
    print()

    for result in results:
        status_tag = f"[{result.status}]"
        print(f"{status_tag} {result.component}")
        print(f"  {result.message}")
        if result.remediation:
            print(f"  Remediation: {result.remediation}")
        print()

    # Kiro Powers informational note
    print("NOTE: Kiro Powers (IDE extensions) cannot be verified programmatically.")
    print("  Please ensure the following Kiro Powers are installed manually:")
    print("  - AWS AgentCore Power")
    print("  - Strands Power")
    print("  - AWS Observability Power")
    print()

    passed = sum(1 for r in results if r.status == "PASS")
    total = len(results)
    overall = "PASS" if passed == total else "FAIL"

    print("============================")
    print(f"Overall: {overall} ({passed}/{total} checks passed)")


def main():
    results = []

    # Check Python dependencies
    dependencies = [
        ("strands_agents", "strands-agents"),
        ("streamlit", "streamlit"),
        ("boto3", "boto3"),
    ]
    for module_name, display_name in dependencies:
        results.append(check_python_dependency(module_name, display_name))

    # Check AWS credentials
    results.append(check_aws_credentials())

    # Check MCP configuration
    results.append(check_mcp_config())

    # Print results
    print_results(results)

    # Exit with appropriate code
    all_passed = all(r.status == "PASS" for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
