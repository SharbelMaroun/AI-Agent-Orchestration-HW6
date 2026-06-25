"""Tests for MCP token auth (mint / verify / revoke)."""

import pytest

from marl_cop_thief.shared.mcp_auth import TokenAuth


def test_mint_then_verify_returns_subject():
    auth = TokenAuth("s3cret")
    token = auth.mint("cop")
    assert auth.verify(token) == "cop"


def test_two_tokens_are_distinct():
    auth = TokenAuth("s3cret")
    assert auth.mint("cop") != auth.mint("cop")  # random nonce per token


def test_tampered_token_is_rejected():
    auth = TokenAuth("s3cret")
    token = auth.mint("cop")
    tampered = token[:-1] + ("0" if token[-1] != "0" else "1")
    assert auth.verify(tampered) is None


def test_token_from_another_secret_is_rejected():
    other = TokenAuth("different").mint("cop")
    assert TokenAuth("s3cret").verify(other) is None


def test_revoked_token_is_rejected():
    auth = TokenAuth("s3cret")
    token = auth.mint("thief")
    assert auth.verify(token) == "thief"
    auth.revoke(token)
    assert auth.verify(token) is None


def test_malformed_or_empty_tokens_are_rejected():
    auth = TokenAuth("s3cret")
    assert auth.verify("") is None
    assert auth.verify("no-dot-here") is None
    assert auth.verify("a:b.deadbeef") is None  # wrong signature


def test_empty_secret_is_rejected():
    with pytest.raises(ValueError, match="non-empty"):
        TokenAuth("")
