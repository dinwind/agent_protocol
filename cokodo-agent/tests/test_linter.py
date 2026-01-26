"""Tests for linter module."""

import json
import tempfile
from pathlib import Path

import pytest

from cokodo_agent.linter import LintResult, ProtocolLinter, update_checksums


class TestLintResult:
    """Test LintResult named tuple."""

    def test_lint_result_creation(self):
        """Test creating a LintResult."""
        result = LintResult(
            rule="test-rule",
            passed=True,
            message="Test message",
            file="test.md",
            line=10,
        )
        assert result.rule == "test-rule"
        assert result.passed is True
        assert result.message == "Test message"
        assert result.file == "test.md"
        assert result.line == 10

    def test_lint_result_defaults(self):
        """Test LintResult default values."""
        result = LintResult(rule="test", passed=True, message="msg")
        assert result.file is None
        assert result.line is None


class TestProtocolLinter:
    """Test ProtocolLinter class."""

    @pytest.fixture
    def temp_agent_dir(self):
        """Create a temporary .agent directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            # Create standard directories
            for dir_name in ProtocolLinter.STANDARD_DIRS:
                (agent_dir / dir_name).mkdir()

            # Create required files
            (agent_dir / "start-here.md").write_text("# Start Here\n", encoding="utf-8")
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": {}}, indent=2),
                encoding="utf-8",
            )

            # Create required project files
            for file_name in ProtocolLinter.REQUIRED_PROJECT_FILES:
                (agent_dir / "project" / file_name).write_text(f"# {file_name}\n", encoding="utf-8")

            yield agent_dir

    def test_init(self, temp_agent_dir):
        """Test linter initialization."""
        linter = ProtocolLinter(temp_agent_dir)
        assert linter.agent_dir == temp_agent_dir
        assert linter.results == []
        assert isinstance(linter.manifest, dict)

    def test_load_manifest(self, temp_agent_dir):
        """Test manifest loading."""
        linter = ProtocolLinter(temp_agent_dir)
        assert linter.manifest.get("version") == "3.0.0"

    def test_load_manifest_missing(self):
        """Test manifest loading when file is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            linter = ProtocolLinter(Path(tmpdir))
            assert linter.manifest == {}

    def test_compute_sha256(self, temp_agent_dir):
        """Test SHA256 computation."""
        test_file = temp_agent_dir / "test.txt"
        test_file.write_text("hello world", encoding="utf-8")

        hash_value = ProtocolLinter.compute_sha256(test_file)
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA256 hex length

    def test_compute_sha256_consistent(self, temp_agent_dir):
        """Test SHA256 is consistent for same content."""
        test_file = temp_agent_dir / "test.txt"
        test_file.write_text("consistent content", encoding="utf-8")

        hash1 = ProtocolLinter.compute_sha256(test_file)
        hash2 = ProtocolLinter.compute_sha256(test_file)
        assert hash1 == hash2

    def test_check_directory_structure_pass(self, temp_agent_dir):
        """Test directory structure check passes."""
        linter = ProtocolLinter(temp_agent_dir)
        linter.check_directory_structure()

        passed = [r for r in linter.results if r.passed]
        assert len(passed) == len(ProtocolLinter.STANDARD_DIRS)

    def test_check_directory_structure_fail(self):
        """Test directory structure check fails for missing dirs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            linter = ProtocolLinter(agent_dir)
            linter.check_directory_structure()

            failed = [r for r in linter.results if not r.passed]
            assert len(failed) == len(ProtocolLinter.STANDARD_DIRS)

    def test_check_required_files_pass(self, temp_agent_dir):
        """Test required files check passes."""
        linter = ProtocolLinter(temp_agent_dir)
        linter.check_required_files()

        failed = [r for r in linter.results if not r.passed]
        assert len(failed) == 0

    def test_check_required_files_missing_project_dir(self):
        """Test required files check when project/ is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            linter = ProtocolLinter(agent_dir)
            linter.check_required_files()

            failed = [r for r in linter.results if not r.passed]
            assert any("project/ directory does not exist" in r.message for r in failed)

    def test_check_naming_convention_pass(self, temp_agent_dir):
        """Test naming convention check for valid names."""
        # Create files with valid kebab-case names
        (temp_agent_dir / "core" / "valid-name.md").write_text("# Valid", encoding="utf-8")
        (temp_agent_dir / "core" / "another-valid.md").write_text("# Valid", encoding="utf-8")

        linter = ProtocolLinter(temp_agent_dir)
        linter.check_naming_convention()

        # Check that valid files pass
        core_results = [r for r in linter.results if "core" in str(r.file)]
        passed = [r for r in core_results if r.passed]
        assert len(passed) >= 2

    def test_check_naming_convention_fail(self, temp_agent_dir):
        """Test naming convention check for invalid names."""
        # Create file with invalid name (camelCase)
        (temp_agent_dir / "core" / "InvalidName.md").write_text("# Invalid", encoding="utf-8")

        linter = ProtocolLinter(temp_agent_dir)
        linter.check_naming_convention()

        failed = [r for r in linter.results if not r.passed and "InvalidName" in str(r.file)]
        assert len(failed) == 1
        assert "kebab-case" in failed[0].message

    def test_check_naming_convention_exceptions(self, temp_agent_dir):
        """Test naming convention allows exceptions."""
        # Create exception files
        (temp_agent_dir / "skills").mkdir(exist_ok=True)
        (temp_agent_dir / "skills" / "SKILL.md").write_text("# Skill", encoding="utf-8")
        (temp_agent_dir / "README.md").write_text("# README", encoding="utf-8")

        linter = ProtocolLinter(temp_agent_dir)
        linter.check_naming_convention()

        # Exception files should not appear as failures
        failed = [r for r in linter.results if not r.passed]
        failed_files = [r.file for r in failed]
        assert "SKILL.md" not in str(failed_files)
        assert "README.md" not in str(failed_files)

    def test_lint_all(self, temp_agent_dir):
        """Test lint_all runs all checks."""
        linter = ProtocolLinter(temp_agent_dir)
        results = linter.lint_all()

        assert len(results) > 0
        assert all(isinstance(r, LintResult) for r in results)

    def test_lint_rule_specific(self, temp_agent_dir):
        """Test lint_rule runs specific check."""
        linter = ProtocolLinter(temp_agent_dir)
        results = linter.lint_rule("directory-structure")

        assert len(results) == len(ProtocolLinter.STANDARD_DIRS)
        assert all(r.rule == "directory-structure" for r in results)

    def test_lint_rule_invalid(self, temp_agent_dir):
        """Test lint_rule with invalid rule name."""
        linter = ProtocolLinter(temp_agent_dir)
        results = linter.lint_rule("invalid-rule")

        assert len(results) == 0

    def test_get_all_locked_files(self, temp_agent_dir):
        """Test getting all locked files."""
        # Create some files in locked directories
        (temp_agent_dir / "core" / "test.md").write_text("# Test", encoding="utf-8")
        (temp_agent_dir / "meta" / "info.md").write_text("# Info", encoding="utf-8")

        linter = ProtocolLinter(temp_agent_dir)
        locked_files = linter.get_all_locked_files()

        assert isinstance(locked_files, list)
        assert "start-here.md" in locked_files
        assert "core/test.md" in locked_files
        assert "meta/info.md" in locked_files

    def test_generate_checksums(self, temp_agent_dir):
        """Test checksum generation."""
        (temp_agent_dir / "core" / "test.md").write_text("# Test", encoding="utf-8")

        linter = ProtocolLinter(temp_agent_dir)
        checksums = linter.generate_checksums()

        assert isinstance(checksums, dict)
        assert "start-here.md" in checksums
        assert "core/test.md" in checksums
        assert all(len(v) == 64 for v in checksums.values())


class TestUpdateChecksums:
    """Test update_checksums function."""

    def test_update_checksums(self):
        """Test updating checksums in manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            # Create minimal structure
            (agent_dir / "core").mkdir()
            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}, indent=2),
                encoding="utf-8",
            )

            checksums = update_checksums(agent_dir)

            assert isinstance(checksums, dict)
            assert "start-here.md" in checksums
            assert "core/rules.md" in checksums

            # Verify manifest was updated
            manifest = json.loads((agent_dir / "manifest.json").read_text(encoding="utf-8"))
            assert "checksums" in manifest
            assert manifest["checksums"] == checksums

    def test_update_checksums_missing_manifest(self):
        """Test update_checksums raises error when manifest missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                update_checksums(Path(tmpdir))


class TestIntegrityCheck:
    """Test integrity checking functionality."""

    def test_check_integrity_pass(self):
        """Test integrity check passes with valid checksums."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "core").mkdir()

            # Create files
            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")

            # Generate checksums
            linter = ProtocolLinter(agent_dir)
            checksums = linter.generate_checksums()

            # Write manifest with checksums
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": checksums}, indent=2),
                encoding="utf-8",
            )

            # Run integrity check
            linter2 = ProtocolLinter(agent_dir)
            linter2.check_integrity()

            failed = [r for r in linter2.results if not r.passed]
            assert len(failed) == 0

    def test_check_integrity_modified_file(self):
        """Test integrity check detects modified files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()
            (agent_dir / "core").mkdir()

            # Create files
            (agent_dir / "start-here.md").write_text("# Start", encoding="utf-8")
            (agent_dir / "core" / "rules.md").write_text("# Rules", encoding="utf-8")

            # Generate checksums
            linter = ProtocolLinter(agent_dir)
            checksums = linter.generate_checksums()

            # Write manifest with checksums
            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0", "checksums": checksums}, indent=2),
                encoding="utf-8",
            )

            # Modify a file
            (agent_dir / "core" / "rules.md").write_text("# Modified Rules", encoding="utf-8")

            # Run integrity check
            linter2 = ProtocolLinter(agent_dir)
            linter2.check_integrity()

            failed = [r for r in linter2.results if not r.passed]
            assert len(failed) == 1
            assert "hash mismatch" in failed[0].message

    def test_check_integrity_no_checksums(self):
        """Test integrity check reports missing checksums."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_dir = Path(tmpdir) / ".agent"
            agent_dir.mkdir()

            (agent_dir / "manifest.json").write_text(
                json.dumps({"version": "3.0.0"}, indent=2),
                encoding="utf-8",
            )

            linter = ProtocolLinter(agent_dir)
            linter.check_integrity()

            failed = [r for r in linter.results if not r.passed]
            assert len(failed) == 1
            assert "No checksums found" in failed[0].message
