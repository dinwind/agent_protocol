"""Tests for fetcher module."""

import pytest
from pathlib import Path

from cokodo_agent.fetcher.builtin import BuiltinFetcher
from cokodo_agent.fetcher.base import SourceUnavailableError


class TestBuiltinFetcher:
    """Test built-in protocol fetcher."""
    
    def test_is_available(self):
        """Test that bundled protocol is available."""
        fetcher = BuiltinFetcher()
        assert fetcher.is_available() is True
    
    def test_fetch_returns_path_and_version(self):
        """Test fetch returns valid path and version."""
        fetcher = BuiltinFetcher()
        path, version = fetcher.fetch()
        
        assert isinstance(path, Path)
        assert path.exists()
        assert (path / "start-here.md").exists()
        assert isinstance(version, str)
        assert len(version) > 0


class TestGitHubFetcher:
    """Test GitHub release fetcher."""
    
    def test_is_available_returns_bool(self):
        """Test is_available returns boolean."""
        from cokodo_agent.fetcher.github import GitHubReleaseFetcher
        
        fetcher = GitHubReleaseFetcher()
        result = fetcher.is_available()
        assert isinstance(result, bool)
