"""Tests for CLI module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from cokodo_agent.cli import app, find_agent_dir

runner = CliRunner()


class TestFindAgentDir:
    """Test find_agent_dir function."""

    def test_find_agent_dir_exists(self):
        """Test finding .agent directory when it exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            result = find_agent_dir(Path(tmpdir))
            assert result == agent_dir

    def test_find_agent_dir_not_found(self):
        """Test finding .agent directory when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError) as exc_info:
                find_agent_dir(Path(tmpdir))
            assert ".agent directory not found" in str(exc_info.value)

    def test_find_agent_dir_default_cwd(self):
        """Test finding .agent directory from current directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            with patch("cokodo_agent.cli.Path.cwd", return_value=Path(tmpdir)):
                result = find_agent_dir(None)
                assert result == agent_dir


class TestVersionCommand:
    """Test version command."""

    def test_version_command(self):
        """Test version command output."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "cokodo-agent" in result.output
        assert "Built-in:" in result.output


class TestInitCommand:
    """Test init command."""

    @patch("cokodo_agent.cli.get_protocol")
    @patch("cokodo_agent.cli.generate_protocol")
    def test_init_with_defaults(self, mock_generate, mock_get_protocol):
        """Test init command with --yes flag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup mock
            protocol_dir = Path(tmpdir) / "protocol"
            protocol_dir.mkdir()
            mock_get_protocol.return_value = (protocol_dir, "3.0.0")

            target_dir = Path(tmpdir) / "project"
            target_dir.mkdir()

            result = runner.invoke(app, ["init", str(target_dir), "--yes"])

            assert result.exit_code == 0
            assert mock_generate.called

    @patch("cokodo_agent.cli.get_protocol")
    def test_init_existing_agent_dir(self, mock_get_protocol):
        """Test init fails when .agent already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create existing .agent
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            result = runner.invoke(app, ["init", str(tmpdir), "--yes"])

            assert result.exit_code == 1
            assert "already exists" in result.output

    @patch("cokodo_agent.cli.get_protocol")
    @patch("cokodo_agent.cli.generate_protocol")
    def test_init_force_overwrite(self, mock_generate, mock_get_protocol):
        """Test init with --force overwrites existing .agent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create existing .agent
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            # Setup mock
            protocol_dir = Path(tmpdir) / "protocol"
            protocol_dir.mkdir()
            mock_get_protocol.return_value = (protocol_dir, "3.0.0")

            result = runner.invoke(app, ["init", str(tmpdir), "--yes", "--force"])

            assert result.exit_code == 0
            assert mock_generate.called


class TestLintCommand:
    """Test lint command."""

    def test_lint_no_agent_dir(self):
        """Test lint fails when .agent doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["lint", str(tmpdir)])

            assert result.exit_code == 1
            assert "not found" in result.output

    def test_lint_basic(self):
        """Test lint command with valid .agent directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal .agent structure
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            for dir_name in ["core", "adapters", "meta", "scripts", "skills", "project"]:
                (agent_dir / dir_name).mkdir()

            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}),
                encoding="utf-8",
            )

            for file_name in [
                "context.md",
                "tech-stack.md",
                "known-issues.md",
                "commands.md",
                "session-journal.md",
            ]:
                (agent_dir / "project" / file_name).write_text(f"# {file_name}", encoding="utf-8")

            result = runner.invoke(app, ["lint", str(tmpdir)])

            # Should run without crashing
            assert "directory-structure" in result.output or "required-files" in result.output

    def test_lint_json_format(self):
        """Test lint command with JSON output format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal .agent structure
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            for dir_name in ["core", "adapters", "meta", "scripts", "skills", "project"]:
                (agent_dir / dir_name).mkdir()

            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}),
                encoding="utf-8",
            )

            result = runner.invoke(app, ["lint", str(tmpdir), "--format", "json"])

            # Output should be valid JSON
            try:
                parsed = json.loads(result.output)
                assert isinstance(parsed, list)
            except json.JSONDecodeError:
                pytest.fail("Output is not valid JSON")

    def test_lint_specific_rule(self):
        """Test lint command with specific rule."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            for dir_name in ["core", "adapters", "meta", "scripts", "skills", "project"]:
                (agent_dir / dir_name).mkdir()

            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            result = runner.invoke(app, ["lint", str(tmpdir), "--rule", "directory-structure"])

            assert "directory-structure" in result.output


class TestUpdateChecksumsCommand:
    """Test update-checksums command."""

    def test_update_checksums_no_agent_dir(self):
        """Test update-checksums fails when .agent doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["update-checksums", str(tmpdir)])

            assert result.exit_code == 1
            assert "not found" in result.output

    def test_update_checksums_success(self):
        """Test update-checksums command succeeds."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "core").mkdir()

            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            result = runner.invoke(app, ["update-checksums", str(tmpdir)])

            assert result.exit_code == 0
            assert "Updated checksums" in result.output

            # Verify manifest was updated
            manifest = json.loads((agent_dir / "manifest.json").read_text(encoding="utf-8"))
            assert "checksums" in manifest


class TestDiffCommand:
    """Test diff command."""

    def test_diff_no_agent_dir(self):
        """Test diff fails when .agent doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["diff", str(tmpdir)])

            assert result.exit_code == 1
            assert "not found" in result.output

    @patch("cokodo_agent.sync.diff_protocol")
    def test_diff_no_changes(self, mock_diff):
        """Test diff command when no changes detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            # Mock no changes
            mock_diff.return_value = ([], "3.0.0", "3.0.0")

            result = runner.invoke(app, ["diff", str(tmpdir)])

            assert result.exit_code == 0
            assert "up to date" in result.output


class TestSyncCommand:
    """Test sync command."""

    def test_sync_no_agent_dir(self):
        """Test sync fails when .agent doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["sync", str(tmpdir)])

            assert result.exit_code == 1
            assert "not found" in result.output

    @patch("cokodo_agent.sync.diff_protocol")
    def test_sync_no_changes(self, mock_diff):
        """Test sync command when no changes needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            # Mock no changes
            mock_diff.return_value = ([], "3.0.0", "3.0.0")

            result = runner.invoke(app, ["sync", str(tmpdir)])

            assert result.exit_code == 0
            assert "up to date" in result.output


class TestContextCommand:
    """Test context command."""

    def test_context_no_agent_dir(self):
        """Test context fails when .agent doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["context", str(tmpdir)])

            assert result.exit_code == 1
            assert "not found" in result.output

    def test_context_no_files(self):
        """Test context command when no files match criteria."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}), encoding="utf-8"
            )

            result = runner.invoke(app, ["context", str(tmpdir)])

            assert result.exit_code == 0
            assert "No context files found" in result.output

    def test_context_with_strategy(self):
        """Test context command with loading strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            manifest = {
                "version": "3.0.0",
                "loading_strategy": {
                    "layers": {
                        "essential": {"files": ["start-here.md"]},
                        "context": {"files": ["project/context.md"]},
                    }
                },
            }
            (agent_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "project").mkdir()
            (agent_dir / "project" / "context.md").write_text("# Context", encoding="utf-8")

            result = runner.invoke(app, ["context", str(tmpdir)])

            assert result.exit_code == 0
            assert "start-here.md" in result.output

    def test_context_paths_output(self):
        """Test context command with paths output format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            manifest = {
                "version": "3.0.0",
                "loading_strategy": {"layers": {"essential": {"files": ["start-here.md"]}}},
            }
            (agent_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")

            result = runner.invoke(app, ["context", str(tmpdir), "--output", "paths"])

            assert result.exit_code == 0
            # Should output absolute path
            assert "start-here.md" in result.output


class TestJournalCommand:
    """Test journal command."""

    def test_journal_no_agent_dir(self):
        """Test journal fails when .agent doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["journal", str(tmpdir), "--title", "Test"])

            assert result.exit_code == 1
            assert "not found" in result.output

    def test_journal_no_journal_file(self):
        """Test journal fails when session-journal.md doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "project").mkdir()

            result = runner.invoke(app, ["journal", str(tmpdir), "--title", "Test"])

            assert result.exit_code == 1
            assert "session-journal.md not found" in result.output

    def test_journal_add_entry(self):
        """Test journal command adds entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "project").mkdir()

            journal_content = """# Session Journal

*Append new sessions below this line.*
"""
            (agent_dir / "project" / "session-journal.md").write_text(
                journal_content, encoding="utf-8"
            )

            result = runner.invoke(
                app,
                [
                    "journal",
                    str(tmpdir),
                    "--title",
                    "Test Session",
                    "--completed",
                    "Task 1, Task 2",
                    "--debt",
                    "Refactor needed",
                    "--decisions",
                    "Use pattern X",
                ],
            )

            assert result.exit_code == 0
            assert "Added session entry" in result.output

            # Verify entry was added
            content = (agent_dir / "project" / "session-journal.md").read_text(encoding="utf-8")
            assert "Test Session" in content
            assert "Task 1" in content
            assert "Refactor needed" in content
            assert "Use pattern X" in content


class TestHelpCommand:
    """Test help command."""

    def test_help_overview(self):
        """Test help command shows overview."""
        result = runner.invoke(app, ["help"])

        assert result.exit_code == 0
        assert "Cokodo Agent" in result.output
        assert "Commands:" in result.output
        assert "init" in result.output
        assert "lint" in result.output
        assert "sync" in result.output

    def test_help_specific_command(self):
        """Test help for specific command."""
        result = runner.invoke(app, ["help", "init"])

        assert result.exit_code == 0
        assert "co init" in result.output
        assert "Description:" in result.output
        assert "Usage:" in result.output
        assert "Options:" in result.output
        assert "Examples:" in result.output
        assert "--yes" in result.output
        assert "--force" in result.output

    def test_help_unknown_command(self):
        """Test help for unknown command."""
        result = runner.invoke(app, ["help", "unknown"])

        assert result.exit_code == 1
        assert "Unknown command" in result.output

    def test_help_all_commands(self):
        """Test help shows all command categories."""
        result = runner.invoke(app, ["help"])

        assert result.exit_code == 0
        assert "Setup" in result.output
        assert "Protocol Management" in result.output
        assert "Development" in result.output
        assert "Information" in result.output
