"""Unit tests for IDE instruction file parsers."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from cokodo_agent.config import IDE_SPEC_VERSIONS
from cokodo_agent.parser import HybridParser, ParsedInstruction
from cokodo_agent.parser.base import (
    extract_agent_references,
    extract_frontmatter,
    extract_imports,
    extract_project_name,
    extract_rules,
    extract_sections,
)
from cokodo_agent.parser.claude import ClaudeParser
from cokodo_agent.parser.copilot import CopilotParser
from cokodo_agent.parser.cursor import CursorParser
from cokodo_agent.parser.gemini import GeminiParser


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def project_with_agent() -> Path:
    """Minimal project with .agent for generator output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / ".agent").mkdir()
        (root / ".agent" / "project").mkdir()
        (root / ".agent" / "project" / "context.md").write_text(
            "# Project Context\n\n## Project Name\n\nTestProject\n",
            encoding="utf-8",
        )
        yield root


# ---------------------------------------------------------------------------
# Base extraction helpers
# ---------------------------------------------------------------------------

class TestExtractFrontmatter:
    def test_no_frontmatter(self) -> None:
        content = "# Hello\n\nBody"
        fm, body = extract_frontmatter(content)
        assert fm == {}
        assert "Hello" in body

    def test_with_frontmatter(self) -> None:
        content = "---\ndescription: Foo\nalwaysApply: true\n---\n\n# Body"
        fm, body = extract_frontmatter(content)
        assert fm.get("description") == "Foo"
        assert fm.get("alwaysApply") is True
        assert "# Body" in body


class TestExtractAgentReferences:
    def test_finds_agent_paths(self) -> None:
        text = "Read .agent/start-here.md and .agent/project/context.md"
        refs = extract_agent_references(text)
        assert "start-here.md" in refs[0] or "start-here.md" in str(refs)
        assert any("context.md" in r for r in refs)

    def test_deduplicates(self) -> None:
        text = ".agent/start-here.md and again .agent/start-here.md"
        refs = extract_agent_references(text)
        assert len(refs) == 1


class TestExtractSections:
    def test_splits_by_h2(self) -> None:
        content = "## Key Rules\n- UTF-8\n- Slash\n\n## Other\n- Foo"
        sections = extract_sections(content)
        assert "Key Rules" in sections
        assert "UTF-8" in sections["Key Rules"]
        assert "Other" in sections


class TestExtractRules:
    def test_extracts_bullets_under_key_rules(self) -> None:
        content = "## Key Rules\n\n- Encoding: UTF-8\n- Paths: forward slash"
        rules = extract_rules(content)
        assert any("UTF-8" in r for r in rules)
        assert any("slash" in r for r in rules)


class TestExtractProjectName:
    def test_first_h1(self) -> None:
        content = "# MyProject\n\n## Section"
        assert extract_project_name(content) == "MyProject"


class TestExtractImports:
    def test_gemini_imports(self) -> None:
        content = "Line\n@.agent/start-here.md\n@.agent/project/context.md"
        imports = extract_imports(content)
        assert "@.agent/start-here.md" in imports
        assert "@.agent/project/context.md" in imports


# ---------------------------------------------------------------------------
# CursorParser
# ---------------------------------------------------------------------------

class TestCursorParser:
    def test_detect_empty(self, project_with_agent: Path) -> None:
        assert CursorParser().detect(project_with_agent) == []

    def test_detect_mdc(self, project_with_agent: Path) -> None:
        rules_dir = project_with_agent / ".cursor" / "rules"
        rules_dir.mkdir(parents=True)
        (rules_dir / "agent-protocol.mdc").write_text("---\ndescription: x\n---\n# Body", encoding="utf-8")
        detected = CursorParser().detect(project_with_agent)
        assert len(detected) == 1
        assert detected[0].format_version == "current"
        assert detected[0].path.endswith(".mdc")

    def test_detect_legacy(self, project_with_agent: Path) -> None:
        (project_with_agent / ".cursorrules").write_text("# Cursor rules", encoding="utf-8")
        detected = CursorParser().detect(project_with_agent)
        assert len(detected) == 1
        assert detected[0].format_version == "legacy"
        assert detected[0].path == ".cursorrules"

    def test_parse_mdc(self, project_with_agent: Path) -> None:
        rules_dir = project_with_agent / ".cursor" / "rules"
        rules_dir.mkdir(parents=True)
        mdc = rules_dir / "agent-protocol.mdc"
        mdc.write_text(
            "---\ndescription: Protocol for MyApp\nalwaysApply: true\n---\n# Agent Protocol\n\n.agent/start-here.md",
            encoding="utf-8",
        )
        parsed = CursorParser().parse_file(mdc, project_with_agent)
        assert parsed.tool_name == "cursor"
        assert parsed.format_version == "current"
        assert parsed.ide_spec_version != "unknown"
        assert parsed.ide_spec_version == IDE_SPEC_VERSIONS["cursor"]["spec_version"]
        assert parsed.frontmatter.get("alwaysApply") is True
        assert "start-here.md" in str(parsed.referenced_files)


# ---------------------------------------------------------------------------
# ClaudeParser
# ---------------------------------------------------------------------------

class TestClaudeParser:
    def test_detect_claude_md(self, project_with_agent: Path) -> None:
        (project_with_agent / "CLAUDE.md").write_text("# MyApp\n\nBody", encoding="utf-8")
        detected = ClaudeParser().detect(project_with_agent)
        assert len(detected) >= 1
        assert any(d.path == "CLAUDE.md" for d in detected)

    def test_parse_claude_md(self, project_with_agent: Path) -> None:
        claude_md = project_with_agent / "CLAUDE.md"
        claude_md.write_text("# MyApp\n\nRead .agent/start-here.md", encoding="utf-8")
        parsed = ClaudeParser().parse_file(claude_md, project_with_agent)
        assert parsed.tool_name == "claude"
        assert parsed.project_name == "MyApp"
        assert any("start-here" in r for r in parsed.referenced_files)


# ---------------------------------------------------------------------------
# CopilotParser
# ---------------------------------------------------------------------------

class TestCopilotParser:
    def test_detect_agents_md(self, project_with_agent: Path) -> None:
        (project_with_agent / "AGENTS.md").write_text("# App\n\nBody", encoding="utf-8")
        detected = CopilotParser().detect(project_with_agent)
        assert len(detected) == 1
        assert detected[0].path == "AGENTS.md"

    def test_parse_agents_md(self, project_with_agent: Path) -> None:
        agents = project_with_agent / "AGENTS.md"
        agents.write_text("# MyApp\n\n.agent/start-here.md", encoding="utf-8")
        parsed = CopilotParser().parse_file(agents, project_with_agent)
        assert parsed.tool_name == "copilot"
        assert parsed.project_name == "MyApp"


# ---------------------------------------------------------------------------
# GeminiParser
# ---------------------------------------------------------------------------

class TestGeminiParser:
    def test_detect_gemini_md(self, project_with_agent: Path) -> None:
        (project_with_agent / "GEMINI.md").write_text("# App\n\n@.agent/start-here.md", encoding="utf-8")
        detected = GeminiParser().detect(project_with_agent)
        assert len(detected) == 1
        assert detected[0].path == "GEMINI.md"

    def test_parse_gemini_imports(self, project_with_agent: Path) -> None:
        gemini = project_with_agent / "GEMINI.md"
        gemini.write_text("# App\n\n@.agent/start-here.md\n\n@.agent/project/context.md", encoding="utf-8")
        parsed = GeminiParser().parse_file(gemini, project_with_agent)
        assert parsed.tool_name == "gemini"
        assert len(parsed.imports) >= 1
        assert any("start-here" in i for i in parsed.imports)


# ---------------------------------------------------------------------------
# HybridParser
# ---------------------------------------------------------------------------

class TestHybridParser:
    def test_detect_all_empty(self, project_with_agent: Path) -> None:
        assert HybridParser().detect_all(project_with_agent) == {}

    def test_detect_all_after_generate(self, project_with_agent: Path) -> None:
        from cokodo_agent.generator import generate_adapters_for_tools
        agent_dir = project_with_agent / ".agent"
        generate_adapters_for_tools(project_with_agent, agent_dir, ["cursor", "claude", "copilot", "gemini"])
        detected = HybridParser().detect_all(project_with_agent)
        assert len(detected) == 4
        assert "cursor" in detected
        assert "claude" in detected
        assert "copilot" in detected
        assert "gemini" in detected

    def test_parse_tool_unknown(self, project_with_agent: Path) -> None:
        with pytest.raises(ValueError, match="Unknown tool"):
            HybridParser().parse_tool(project_with_agent, "unknown")
