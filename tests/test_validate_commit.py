"""
test_validate_commit.py - Unit tests for validate-commit.py.
"""

import importlib.util
import os
import sys
import tempfile
import pytest

# Dynamically import validate-commit.py
SCRIPT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "skills",
        "git-commit-helper",
        "scripts",
        "validate-commit.py",
    )
)
spec = importlib.util.spec_from_file_location("validate_commit_mod", SCRIPT_PATH)
validate_commit_mod = importlib.util.module_from_spec(spec)
sys.modules["validate_commit_mod"] = validate_commit_mod
spec.loader.exec_module(validate_commit_mod)


def test_valid_simple_commit():
    """Test standard simple commit message."""
    res = validate_commit_mod.validate_commit_message("feat: add user login endpoint")
    assert res["valid"] is True
    assert res["type"] == "feat"
    assert res["scope"] is None
    assert res["description"] == "add user login endpoint"
    assert res["is_breaking"] is False
    assert len(res["errors"]) == 0


def test_valid_scoped_commit():
    """Test scoped commit message."""
    res = validate_commit_mod.validate_commit_message("fix(auth): handle null session token")
    assert res["valid"] is True
    assert res["type"] == "fix"
    assert res["scope"] == "auth"
    assert res["description"] == "handle null session token"
    assert res["is_breaking"] is False


def test_breaking_change_bang():
    """Test breaking change indicator '!' in header."""
    res = validate_commit_mod.validate_commit_message("feat(api)!: remove v1 endpoints")
    assert res["valid"] is True
    assert res["is_breaking"] is True
    assert res["breaking_description"] == "remove v1 endpoints"


def test_breaking_change_footer():
    """Test breaking change indicated via footer."""
    msg = """feat(api): update authentication scheme

Refactored auth pipeline for improved security.

BREAKING CHANGE: Bearer token is now required on all requests."""
    res = validate_commit_mod.validate_commit_message(msg)
    assert res["valid"] is True
    assert res["is_breaking"] is True
    assert "Bearer token is now required" in res["breaking_description"]
    assert res["body"] == "Refactored auth pipeline for improved security."
    assert len(res["footers"]) == 1
    assert res["footers"][0]["token"] == "BREAKING CHANGE"


def test_empty_message():
    """Test empty commit message."""
    res = validate_commit_mod.validate_commit_message("   ")
    assert res["valid"] is False
    assert any("empty" in e.lower() for e in res["errors"])


def test_invalid_type():
    """Test commit message with disallowed type."""
    res = validate_commit_mod.validate_commit_message("customtype(core): do something")
    assert res["valid"] is False
    assert any("unknown commit type" in e.lower() for e in res["errors"])


def test_uppercase_description_warning():
    """Test warning for uppercase description letter."""
    res = validate_commit_mod.validate_commit_message("feat(ui): Add dark mode toggle")
    # By default, uppercase is a warning, not an error
    assert res["valid"] is True
    assert len(res["warnings"]) > 0
    assert any("uppercase" in w.lower() for w in res["warnings"])
    assert any("add dark mode toggle" in s for s in res["suggestions"])

    # In strict mode, warnings invalidate the commit
    strict_res = validate_commit_mod.validate_commit_message(
        "feat(ui): Add dark mode toggle",
        strict=True,
    )
    assert strict_res["valid"] is False


def test_trailing_period_error():
    """Test error for trailing period in description."""
    res = validate_commit_mod.validate_commit_message("docs: update api reference.")
    assert res["valid"] is False
    assert any("period" in e.lower() for e in res["errors"])
    assert any("docs: update api reference" in s for s in res["suggestions"])


def test_missing_blank_line_after_header():
    """Test error when second line is not blank before body."""
    msg = """feat(cli): add verbose flag
This line is placed directly below the header without blank line."""
    res = validate_commit_mod.validate_commit_message(msg)
    assert res["valid"] is False
    assert any("must be blank" in e.lower() for e in res["errors"])


def test_file_input_validation():
    """Test reading commit message from file."""
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
        tf.write("refactor(db): optimize connection pool query\n\nReplaces linear search with indexed lookup.")
        tf_path = tf.name

    try:
        with open(tf_path, "r", encoding="utf-8") as f:
            content = f.read()
        res = validate_commit_mod.validate_commit_message(content)
        assert res["valid"] is True
        assert res["type"] == "refactor"
        assert res["scope"] == "db"
        assert res["body"] == "Replaces linear search with indexed lookup."
    finally:
        os.remove(tf_path)
