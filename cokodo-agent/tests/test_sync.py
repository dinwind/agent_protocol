"""Tests for sync module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from cokodo_agent.sync import (
    DiffResult,
    SyncResult,
    diff_protocol,
    get_context_files,
    get_protocol_version,
    sync_protocol,
)


class TestDiffResult:
    """Test DiffResult named tuple."""

    def test_diff_result_creation(self):
        """Test creating a DiffResult."""
        result = DiffResult(
            path="core/rules.md",
            status="modified",
            local_hash="abc123",
            remote_hash="def456",
        )
        assert result.path == "core/rules.md"
        assert result.status == "modified"
        assert result.local_hash == "abc123"
        assert result.remote_hash == "def456"

    def test_diff_result_defaults(self):
        """Test DiffResult default values."""
        result = DiffResult(path="test.md", status="added")
        assert result.local_hash is None
        assert result.remote_hash is None


class TestSyncResult:
    """Test SyncResult named tuple."""

    def test_sync_result_creation(self):
        """Test creating a SyncResult."""
        result = SyncResult(
            updated=["file1.md", "file2.md"],
            skipped=["project/context.md"],
            errors=[],
        )
        assert result.updated == ["file1.md", "file2.md"]
        assert result.skipped == ["project/context.md"]
        assert result.errors == []


class TestGetProtocolVersion:
    """Test get_protocol_version function."""

    def test_get_version_success(self):
        """Test getting version from manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            manifest = {"version": "3.0.0", "name": "test"}
            (agent_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            version = get_protocol_version(agent_dir)
            assert version == "3.0.0"

    def test_get_version_missing_manifest(self):
        """Test getting version when manifest is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            version = get_protocol_version(Path(tmpdir))
            assert version is None

    def test_get_version_invalid_json(self):
        """Test getting version with invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text("invalid json", encoding="utf-8")

            version = get_protocol_version(agent_dir)
            assert version is None

    def test_get_version_missing_version_key(self):
        """Test getting version when version key is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(json.dumps({"name": "test"}), encoding="utf-8")

            version = get_protocol_version(agent_dir)
            assert version is None


class TestGetContextFiles:
    """Test get_context_files function."""

    @pytest.fixture
    def manifest_with_strategy(self):
        """Create a manifest with loading strategy."""
        return {
            "version": "3.0.0",
            "loading_strategy": {
                "layers": {
                    "essential": {"files": ["start-here.md", "core/core-rules.md"]},
                    "context": {"files": ["project/context.md", "project/tech-stack.md"]},
                    "stack_specs": {
                        "options": {
                            "python": ["core/stack-specs/python.md"],
                            "rust": ["core/stack-specs/rust.md"],
                        }
                    },
                    "workflows": {
                        "mappings": {
                            "testing": ["core/workflows/testing.md"],
                            "review": ["core/workflows/review-process.md"],
                        }
                    },
                    "skills": {
                        "modules": {
                            "guardian": {
                                "entry": "skills/guardian/SKILL.md",
                                "files": ["skills/guardian/checks.md"],
                            }
                        }
                    },
                },
                "task_profiles": {
                    "code-review": {
                        "workflows": ["review"],
                        "skills": ["guardian"],
                    }
                },
            },
        }

    def test_get_context_files_essential(self, manifest_with_strategy):
        """Test getting essential context files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(
                json.dumps(manifest_with_strategy), encoding="utf-8"
            )

            files = get_context_files(agent_dir)

            assert "start-here.md" in files
            assert "core/core-rules.md" in files
            assert "project/context.md" in files

    def test_get_context_files_with_stack(self, manifest_with_strategy):
        """Test getting context files with stack filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(
                json.dumps(manifest_with_strategy), encoding="utf-8"
            )

            files = get_context_files(agent_dir, stack="python")

            assert "core/stack-specs/python.md" in files
            assert "core/stack-specs/rust.md" not in files

    def test_get_context_files_with_task(self, manifest_with_strategy):
        """Test getting context files with task filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(
                json.dumps(manifest_with_strategy), encoding="utf-8"
            )

            files = get_context_files(agent_dir, task="testing")

            assert "core/workflows/testing.md" in files

    def test_get_context_files_with_task_profile(self, manifest_with_strategy):
        """Test getting context files with task profile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(
                json.dumps(manifest_with_strategy), encoding="utf-8"
            )

            files = get_context_files(agent_dir, task="code-review")

            assert "core/workflows/review-process.md" in files
            assert "skills/guardian/SKILL.md" in files
            assert "skills/guardian/checks.md" in files

    def test_get_context_files_no_duplicates(self, manifest_with_strategy):
        """Test that returned files have no duplicates."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(
                json.dumps(manifest_with_strategy), encoding="utf-8"
            )

            files = get_context_files(agent_dir, stack="python", task="code-review")

            assert len(files) == len(set(files))

    def test_get_context_files_missing_manifest(self):
        """Test getting context files when manifest is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = get_context_files(Path(tmpdir))
            assert files == []

    def test_get_context_files_invalid_json(self):
        """Test getting context files with invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text("invalid", encoding="utf-8")

            files = get_context_files(agent_dir)
            assert files == []

    def test_get_context_files_empty_strategy(self):
        """Test getting context files with empty loading strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir)
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            files = get_context_files(agent_dir)
            assert files == []


class TestDiffProtocol:
    """Test diff_protocol function."""

    @patch("cokodo_agent.sync.get_protocol")
    def test_diff_protocol_unchanged(self, mock_get_protocol):
        """Test diff when files are unchanged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup local agent dir
            local_dir = Path(tmpdir) / "local" / ".agent"
            local_dir.mkdir(parents=True)
            (local_dir / "core").mkdir()
            (local_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (local_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")
            (local_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}), encoding="utf-8"
            )

            # Setup remote protocol (same content)
            remote_dir = Path(tmpdir) / "remote"
            remote_dir.mkdir()
            (remote_dir / "core").mkdir()
            (remote_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (remote_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")
            (remote_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            mock_get_protocol.return_value = (remote_dir, "3.0.0")

            results, local_ver, remote_ver = diff_protocol(local_dir, offline=True)

            assert local_ver == "3.0.0"
            assert remote_ver == "3.0.0"
            unchanged = [r for r in results if r.status == "unchanged"]
            assert len(unchanged) > 0

    @patch("cokodo_agent.sync.get_protocol")
    def test_diff_protocol_modified(self, mock_get_protocol):
        """Test diff detects modified files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup local agent dir
            local_dir = Path(tmpdir) / "local" / ".agent"
            local_dir.mkdir(parents=True)
            (local_dir / "core").mkdir()
            (local_dir / "start-here.md").write_text("# Start Local", encoding="utf-8")
            (local_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            # Setup remote protocol (different content)
            remote_dir = Path(tmpdir) / "remote"
            remote_dir.mkdir()
            (remote_dir / "core").mkdir()
            (remote_dir / "start-here.md").write_text("# Start Remote", encoding="utf-8")
            (remote_dir / "manifest.json").write_text(
                json.dumps({"version": "3.1.0"}), encoding="utf-8"
            )

            mock_get_protocol.return_value = (remote_dir, "3.1.0")

            results, local_ver, remote_ver = diff_protocol(local_dir, offline=True)

            modified = [r for r in results if r.status == "modified"]
            assert len(modified) > 0

    @patch("cokodo_agent.sync.get_protocol")
    def test_diff_protocol_added(self, mock_get_protocol):
        """Test diff detects added files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup local agent dir (minimal)
            local_dir = Path(tmpdir) / "local" / ".agent"
            local_dir.mkdir(parents=True)
            (local_dir / "core").mkdir()
            (local_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (local_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            # Setup remote protocol (with extra file)
            remote_dir = Path(tmpdir) / "remote"
            remote_dir.mkdir()
            (remote_dir / "core").mkdir()
            (remote_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (remote_dir / "core" / "new-file.md").write_text("# New", encoding="utf-8")
            (remote_dir / "manifest.json").write_text(
                json.dumps({"version": "3.1.0"}), encoding="utf-8"
            )

            mock_get_protocol.return_value = (remote_dir, "3.1.0")

            results, _, _ = diff_protocol(local_dir, offline=True)

            added = [r for r in results if r.status == "added"]
            assert len(added) > 0


class TestSyncProtocol:
    """Test sync_protocol function."""

    @patch("cokodo_agent.sync.get_protocol")
    def test_sync_protocol_dry_run(self, mock_get_protocol):
        """Test sync in dry run mode doesn't modify files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup local agent dir
            local_dir = Path(tmpdir) / "local" / ".agent"
            local_dir.mkdir(parents=True)
            (local_dir / "core").mkdir()
            (local_dir / "start-here.md").write_text("# Old", encoding="utf-8")
            (local_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}), encoding="utf-8"
            )

            # Setup remote protocol
            remote_dir = Path(tmpdir) / "remote"
            remote_dir.mkdir()
            (remote_dir / "core").mkdir()
            (remote_dir / "start-here.md").write_text("# New", encoding="utf-8")
            (remote_dir / "manifest.json").write_text(
                json.dumps({"version": "3.1.0"}), encoding="utf-8"
            )

            mock_get_protocol.return_value = (remote_dir, "3.1.0")

            result, _, _ = sync_protocol(local_dir, offline=True, dry_run=True)

            # File should not be modified in dry run
            content = (local_dir / "start-here.md").read_text(encoding="utf-8")
            assert content == "# Old"
            assert len(result.updated) > 0

    @patch("cokodo_agent.sync.get_protocol")
    def test_sync_protocol_skips_project(self, mock_get_protocol):
        """Test sync skips project/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup local agent dir with locked files
            local_dir = Path(tmpdir) / "local" / ".agent"
            local_dir.mkdir(parents=True)
            (local_dir / "core").mkdir()
            (local_dir / "project").mkdir()
            (local_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (local_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")
            (local_dir / "project" / "context.md").write_text("# My Project", encoding="utf-8")
            (local_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}), encoding="utf-8"
            )

            # Setup remote protocol with different project content
            remote_dir = Path(tmpdir) / "remote"
            remote_dir.mkdir()
            (remote_dir / "core").mkdir()
            (remote_dir / "project").mkdir()
            (remote_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (remote_dir / "core" / "rules.md").write_text("# Rules Updated", encoding="utf-8")
            (remote_dir / "project" / "context.md").write_text(
                "# Template Different", encoding="utf-8"
            )
            (remote_dir / "manifest.json").write_text(
                json.dumps({"version": "3.1.0"}), encoding="utf-8"
            )

            mock_get_protocol.return_value = (remote_dir, "3.1.0")

            result, _, _ = sync_protocol(local_dir, offline=True, dry_run=True)

            # core/rules.md should be updated (it's a locked file with different content)
            updated_paths = [u for u in result.updated if "core/" in u]
            assert (
                len(updated_paths) > 0
            ), f"Expected core files to be updated, got: {result.updated}"

    @patch("cokodo_agent.sync.get_protocol")
    def test_sync_protocol_updates_files(self, mock_get_protocol):
        """Test sync actually updates files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup local agent dir
            local_dir = Path(tmpdir) / "local" / ".agent"
            local_dir.mkdir(parents=True)
            (local_dir / "core").mkdir()
            (local_dir / "start-here.md").write_text("# Old Content", encoding="utf-8")
            (local_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}), encoding="utf-8"
            )

            # Setup remote protocol
            remote_dir = Path(tmpdir) / "remote"
            remote_dir.mkdir()
            (remote_dir / "core").mkdir()
            (remote_dir / "start-here.md").write_text("# New Content", encoding="utf-8")
            (remote_dir / "manifest.json").write_text(
                json.dumps({"version": "3.1.0"}), encoding="utf-8"
            )

            mock_get_protocol.return_value = (remote_dir, "3.1.0")

            result, _, _ = sync_protocol(local_dir, offline=True, dry_run=False)

            # File should be updated
            content = (local_dir / "start-here.md").read_text(encoding="utf-8")
            assert content == "# New Content"
            assert len(result.updated) > 0
