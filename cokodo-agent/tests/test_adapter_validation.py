"""Adapter validation tests.

Verifies that each IDE adapter generates files in the correct location,
with the correct format, and that all adapters consistently reference
the same `.agent/` entry point and key documents.

Official specs (as of 2026-02):
- Cursor:  .cursor/rules/*.mdc  with YAML frontmatter
- Claude:  CLAUDE.md            at project root
- Copilot: AGENTS.md            at project root
- Gemini:  GEMINI.md            at project root (supports @file imports)
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

import pytest

from cokodo_agent.config import AI_TOOLS
from cokodo_agent.generator import generate_adapters_for_tools


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def project_dir() -> Path:
    """Create a temporary project with a minimal .agent directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        agent_dir = root / ".agent"
        agent_dir.mkdir()

        # Minimal start-here.md
        (agent_dir / "start-here.md").write_text(
            "# Start Here\nEntry point.\n", encoding="utf-8"
        )

        # project/context.md with a project name
        project_dir = agent_dir / "project"
        project_dir.mkdir()
        (project_dir / "context.md").write_text(
            "# Project Context\n\n## Project Name\n\nTestProject\n",
            encoding="utf-8",
        )

        # core/core-rules.md
        core_dir = agent_dir / "core"
        core_dir.mkdir()
        (core_dir / "core-rules.md").write_text(
            "# Core Rules\nDo not violate.\n", encoding="utf-8"
        )

        yield root


def _generate_all(project_dir: Path) -> dict[str, str]:
    """Generate all adapters and return {tool_key: content} map."""
    agent_dir = project_dir / ".agent"
    tool_keys = [k for k in AI_TOOLS if AI_TOOLS[k].get("file")]
    generate_adapters_for_tools(project_dir, agent_dir, tool_keys)

    contents: dict[str, str] = {}
    for key in tool_keys:
        file_spec = AI_TOOLS[key]["file"]
        if file_spec is None:
            continue
        if file_spec.endswith("/"):
            # Directory mode (cursor) — read the .mdc file inside
            mdc = project_dir / file_spec / "agent-protocol.mdc"
            if mdc.exists():
                contents[key] = mdc.read_text(encoding="utf-8")
        else:
            path = project_dir / file_spec
            if path.exists():
                contents[key] = path.read_text(encoding="utf-8")
    return contents


# ---------------------------------------------------------------------------
# Cursor adapter tests
# ---------------------------------------------------------------------------

class TestCursorAdapter:
    """Cursor: .cursor/rules/agent-protocol.mdc with YAML frontmatter."""

    def test_generates_mdc_file(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])

        mdc = project_dir / ".cursor" / "rules" / "agent-protocol.mdc"
        assert mdc.exists(), ".cursor/rules/agent-protocol.mdc not generated"

    def test_has_yaml_frontmatter(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])

        content = (
            project_dir / ".cursor" / "rules" / "agent-protocol.mdc"
        ).read_text(encoding="utf-8")

        # Must start with YAML frontmatter delimiters
        assert content.startswith("---\n"), "Missing opening YAML frontmatter ---"
        # Must have closing delimiter
        parts = content.split("---\n", 2)
        assert len(parts) >= 3, "Missing closing YAML frontmatter ---"

    def test_frontmatter_has_description(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])

        content = (
            project_dir / ".cursor" / "rules" / "agent-protocol.mdc"
        ).read_text(encoding="utf-8")

        frontmatter = content.split("---\n")[1]
        assert "description:" in frontmatter, "Frontmatter missing 'description' field"

    def test_frontmatter_has_always_apply(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])

        content = (
            project_dir / ".cursor" / "rules" / "agent-protocol.mdc"
        ).read_text(encoding="utf-8")

        frontmatter = content.split("---\n")[1]
        assert "alwaysApply:" in frontmatter, "Frontmatter missing 'alwaysApply' field"
        assert "alwaysApply: true" in frontmatter, "alwaysApply should be true"

    def test_references_start_here(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])

        content = (
            project_dir / ".cursor" / "rules" / "agent-protocol.mdc"
        ).read_text(encoding="utf-8")

        assert ".agent/start-here.md" in content


# ---------------------------------------------------------------------------
# Claude Code adapter tests
# ---------------------------------------------------------------------------

class TestClaudeAdapter:
    """Claude Code: CLAUDE.md at project root."""

    def test_generates_claude_md(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["claude"])

        claude_md = project_dir / "CLAUDE.md"
        assert claude_md.exists(), "CLAUDE.md not generated at project root"

    def test_does_not_generate_old_path(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["claude"])

        old_path = project_dir / ".claude" / "instructions.md"
        assert not old_path.exists(), "Old .claude/instructions.md should not be generated"

    def test_first_line_is_heading(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["claude"])

        content = (project_dir / "CLAUDE.md").read_text(encoding="utf-8")
        first_line = content.strip().split("\n")[0]
        assert first_line.startswith("# "), "CLAUDE.md first line must be an H1 heading"

    def test_references_start_here(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["claude"])

        content = (project_dir / "CLAUDE.md").read_text(encoding="utf-8")
        assert ".agent/start-here.md" in content


# ---------------------------------------------------------------------------
# GitHub Copilot adapter tests
# ---------------------------------------------------------------------------

class TestCopilotAdapter:
    """GitHub Copilot: AGENTS.md at project root."""

    def test_generates_agents_md(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["copilot"])

        agents_md = project_dir / "AGENTS.md"
        assert agents_md.exists(), "AGENTS.md not generated at project root"

    def test_does_not_generate_old_path(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["copilot"])

        old_path = project_dir / ".github" / "copilot-instructions.md"
        assert not old_path.exists(), "Old .github/copilot-instructions.md should not be generated"

    def test_references_start_here(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["copilot"])

        content = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert ".agent/start-here.md" in content


# ---------------------------------------------------------------------------
# Gemini Code Assist adapter tests
# ---------------------------------------------------------------------------

class TestGeminiAdapter:
    """Gemini Code Assist: GEMINI.md at project root with @import syntax."""

    def test_generates_gemini_md(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])

        gemini_md = project_dir / "GEMINI.md"
        assert gemini_md.exists(), "GEMINI.md not generated at project root"

    def test_does_not_generate_old_rules_dir(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])

        old_dir = project_dir / ".agent" / "rules"
        # rules/ directory may exist from other processes but should not be
        # created by the gemini adapter
        rules_files = list(old_dir.glob("*.md")) if old_dir.exists() else []
        # We only check that the adapter didn't create new rule files
        assert not any(
            f.name in ("core-rules.md", "instructions.md", "conventions.md", "security.md")
            for f in rules_files
        ), "Gemini adapter should not create .agent/rules/ files"

    def test_uses_at_import_syntax(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])

        content = (project_dir / "GEMINI.md").read_text(encoding="utf-8")
        # Must contain at least one @.agent/ import
        at_imports = re.findall(r"^@\.agent/.+$", content, re.MULTILINE)
        assert len(at_imports) >= 1, "GEMINI.md must use @.agent/ import syntax"

    def test_imports_start_here(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])

        content = (project_dir / "GEMINI.md").read_text(encoding="utf-8")
        assert "@.agent/start-here.md" in content

    def test_references_start_here(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])

        content = (project_dir / "GEMINI.md").read_text(encoding="utf-8")
        assert ".agent/start-here.md" in content


# ---------------------------------------------------------------------------
# Cross-adapter consistency tests
# ---------------------------------------------------------------------------

class TestCrossAdapterConsistency:
    """All adapters must reference the same entry point and key documents."""

    def test_all_adapters_reference_start_here(self, project_dir: Path) -> None:
        """Every adapter must mention .agent/start-here.md."""
        contents = _generate_all(project_dir)
        assert len(contents) >= 4, f"Expected 4 adapters, got {len(contents)}"

        for tool_key, content in contents.items():
            assert ".agent/start-here.md" in content, (
                f"{tool_key} adapter does not reference .agent/start-here.md"
            )

    def test_all_adapters_reference_context(self, project_dir: Path) -> None:
        """Every adapter must mention .agent/project/context.md."""
        contents = _generate_all(project_dir)

        for tool_key, content in contents.items():
            assert ".agent/project/context.md" in content, (
                f"{tool_key} adapter does not reference .agent/project/context.md"
            )

    def test_all_adapters_reference_core_rules(self, project_dir: Path) -> None:
        """Every adapter must mention .agent/core/core-rules.md."""
        contents = _generate_all(project_dir)

        for tool_key, content in contents.items():
            assert ".agent/core/core-rules.md" in content, (
                f"{tool_key} adapter does not reference .agent/core/core-rules.md"
            )

    def test_all_adapters_mention_utf8(self, project_dir: Path) -> None:
        """Every adapter should mention UTF-8 encoding rule."""
        contents = _generate_all(project_dir)

        for tool_key, content in contents.items():
            assert "utf-8" in content.lower(), (
                f"{tool_key} adapter does not mention UTF-8 encoding"
            )

    def test_config_registry_matches_generators(self, project_dir: Path) -> None:
        """Every tool in AI_TOOLS with a file should produce output."""
        contents = _generate_all(project_dir)
        expected_keys = {k for k, v in AI_TOOLS.items() if v.get("file")}
        assert set(contents.keys()) == expected_keys, (
            f"Mismatch: config has {expected_keys}, generators produced {set(contents.keys())}"
        )


# ---------------------------------------------------------------------------
# Legacy alias tests
# ---------------------------------------------------------------------------

class TestLegacyAlias:
    """Ensure 'antigravity' is handled as an alias for 'gemini'."""

    def test_antigravity_not_in_ai_tools(self) -> None:
        """The old 'antigravity' key should no longer exist in AI_TOOLS."""
        assert "antigravity" not in AI_TOOLS

    def test_gemini_in_ai_tools(self) -> None:
        """The new 'gemini' key must exist in AI_TOOLS."""
        assert "gemini" in AI_TOOLS
        assert AI_TOOLS["gemini"]["file"] == "GEMINI.md"
