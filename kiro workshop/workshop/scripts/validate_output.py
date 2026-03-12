#!/usr/bin/env python3
"""
Validation script for IDP Agent output.

Compares actual IDP Agent output JSON against a reference (expected) JSON file
and reports field-level match results in a formatted table.

Usage:
    python workshop/scripts/validate_output.py \
        --actual output.json \
        --expected workshop/reference/bmr-sample-01-clean-expected.json

Exit codes:
    0 - All fields match
    1 - One or more field mismatches
    2 - File not found or JSON parse error
"""

import argparse
import json
import sys


def flatten_json(obj, prefix=""):
    """Recursively flatten a nested JSON object into dot-notation paths.

    Arrays use bracket notation: ingredients[0].ingredient_name
    Leaf values (strings, numbers, booleans, None) are returned as-is.

    Args:
        obj: The JSON value to flatten (dict, list, or leaf).
        prefix: The current dot-notation path prefix.

    Returns:
        A dict mapping dot-notation field paths to their leaf values.
    """
    fields = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            fields.update(flatten_json(value, path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            path = f"{prefix}[{i}]"
            fields.update(flatten_json(item, path))
    else:
        # Leaf value (str, int, float, bool, None)
        fields[prefix] = obj

    return fields


def compare_json(expected, actual):
    """Compare two JSON objects field by field.

    Args:
        expected: The reference JSON object (dict).
        actual: The actual IDP Agent output JSON object (dict).

    Returns:
        A list of tuples: (field_path, expected_value, actual_value, match).
    """
    expected_fields = flatten_json(expected)
    actual_fields = flatten_json(actual)

    comparisons = []

    for field_path, exp_value in expected_fields.items():
        if field_path in actual_fields:
            act_value = actual_fields[field_path]
            match = exp_value == act_value
            comparisons.append((field_path, exp_value, act_value, match))
        else:
            comparisons.append((field_path, exp_value, "MISSING", False))

    return comparisons


def format_value(value, max_width=20):
    """Format a value for table display, truncating if needed.

    Args:
        value: The value to format.
        max_width: Maximum display width.

    Returns:
        A string representation of the value.
    """
    if value is None:
        text = "null"
    elif value == "MISSING":
        text = "MISSING"
    else:
        text = str(value)

    if len(text) > max_width:
        return text[: max_width - 3] + "..."
    return text


def print_report(comparisons):
    """Print a formatted comparison table.

    Args:
        comparisons: List of (field_path, expected, actual, match) tuples.
    """
    # Calculate column widths
    field_width = max(len("Field"), max((len(c[0]) for c in comparisons), default=5))
    exp_width = max(
        len("Expected"),
        max((len(format_value(c[1])) for c in comparisons), default=8),
    )
    act_width = max(
        len("Actual"),
        max((len(format_value(c[2])) for c in comparisons), default=6),
    )
    match_width = 5  # "Match" header

    # Print header
    header = (
        f"{'Field':<{field_width}} | "
        f"{'Expected':<{exp_width}} | "
        f"{'Actual':<{act_width}} | "
        f"{'Match':<{match_width}}"
    )
    separator = (
        f"{'-' * field_width}-|-"
        f"{'-' * exp_width}-|-"
        f"{'-' * act_width}-|-"
        f"{'-' * match_width}"
    )
    print(header)
    print(separator)

    # Print rows
    for field_path, exp_value, act_value, match in comparisons:
        match_symbol = "\u2713" if match else "\u2717"
        row = (
            f"{field_path:<{field_width}} | "
            f"{format_value(exp_value):<{exp_width}} | "
            f"{format_value(act_value):<{act_width}} | "
            f"{match_symbol}"
        )
        print(row)


def print_summary(comparisons):
    """Print a summary of the comparison results.

    Args:
        comparisons: List of (field_path, expected, actual, match) tuples.
    """
    total = len(comparisons)
    matched = sum(1 for _, _, _, m in comparisons if m)
    mismatched = total - matched
    missing = sum(1 for _, _, a, _ in comparisons if a == "MISSING")

    print()
    print(f"Total fields: {total}")
    print(f"Matched:      {matched}")
    print(f"Mismatched:   {mismatched}")
    if missing > 0:
        print(f"Missing:      {missing}")
    print(f"Result:       {'PASS' if mismatched == 0 else 'FAIL'}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare IDP Agent output JSON against reference JSON."
    )
    parser.add_argument(
        "--actual", required=True, help="Path to the actual IDP Agent output JSON file"
    )
    parser.add_argument(
        "--expected", required=True, help="Path to the expected reference JSON file"
    )
    args = parser.parse_args()

    # Load actual JSON
    try:
        with open(args.actual, "r", encoding="utf-8") as f:
            actual_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Actual file not found: {args.actual}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.actual}: {e}", file=sys.stderr)
        sys.exit(2)

    # Load expected JSON
    try:
        with open(args.expected, "r", encoding="utf-8") as f:
            expected_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Expected file not found: {args.expected}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.expected}: {e}", file=sys.stderr)
        sys.exit(2)

    # Compare
    comparisons = compare_json(expected_data, actual_data)

    # Report
    if not comparisons:
        print("No fields to compare.")
        sys.exit(0)

    print_report(comparisons)
    print_summary(comparisons)

    # Exit code
    all_match = all(m for _, _, _, m in comparisons)
    sys.exit(0 if all_match else 1)


if __name__ == "__main__":
    main()
