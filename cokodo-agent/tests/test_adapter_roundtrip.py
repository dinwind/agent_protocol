"""Round-trip tests: generate adapters -> parse -> assert semantic equivalence."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from cokodo_agent.config import AI_TOOLS
from cokodo_agent.generator import generate_adapters_for_tools
from cokodo_agent.parser import HybridParser, ParsedInstruction


@pytest.fixture()
def project_dir() -> Path:
    """Project with .agent and context containing project name."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        agent_dir = root / ".agent"
        agent_dir.mkdir()
        (agent_dir / "start-here.md").write_text("# Start Here\n", encoding="utf-8")
        (agent_dir / "project").mkdir()
        (agent_dir / "project" / "context.md").write_text(
            "# Project Context\n\n## Project Name\n\nTestProject\n",
            encoding="utf-8",
        )
        (agent_dir / "core").mkdir()
        (agent_dir / "core" / "core-rules.md").write_text("# Core Rules\n", encoding="utf-8")
        yield root


def _generate_all_adapters(project_dir: Path) -> None:
    agent_dir = project_dir / ".agent"
    tool_keys = [k for k in AI_TOOLS if AI_TOOLS[k].get("file")]
    generate_adapters_for_tools(project_dir, agent_dir, tool_keys)


class TestCursorRoundtrip:
    def test_cursor_roundtrip(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "cursor")
        assert len(parsed_list) == 1
        p = parsed_list[0]
        assert p.tool_name == "cursor"
        assert p.format_version == "current"
        assert p.frontmatter.get("alwaysApply") is True
        assert "description" in p.frontmatter
        assert any("start-here" in r for r in p.referenced_files)
        assert any("context.md" in r for r in p.referenced_files)
        assert any("core-rules" in r for r in p.referenced_files)

    def test_cursor_references_start_here(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["cursor"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "cursor")
        p = parsed_list[0]
        assert ".agent/start-here.md" in p.raw_content or any(
            "start-here.md" in r for r in p.referenced_files
        )


class TestClaudeRoundtrip:
    def test_claude_roundtrip(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["claude"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "claude")
        assert len(parsed_list) == 1
        p = parsed_list[0]
        assert p.tool_name == "claude"
        assert p.project_name == "TestProject"
        assert any("start-here" in r for r in p.referenced_files)
        assert any("context" in r for r in p.referenced_files)
        assert "First Step" in p.sections or "Essential Files" in p.sections

    def test_claude_key_rules_present(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["claude"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "claude")
        p = parsed_list[0]
        assert any("UTF-8" in r or "utf-8" in r.lower() for r in p.rules)


class TestCopilotRoundtrip:
    def test_copilot_roundtrip(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["copilot"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "copilot")
        assert len(parsed_list) == 1
        p = parsed_list[0]
        assert p.tool_name == "copilot"
        assert p.project_name == "TestProject"
        assert any("start-here" in r for r in p.referenced_files)


class TestGeminiRoundtrip:
    def test_gemini_roundtrip(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "gemini")
        assert len(parsed_list) == 1
        p = parsed_list[0]
        assert p.tool_name == "gemini"
        assert any("start-here" in i or "start-here" in str(p.imports) for i in p.imports)
        assert any("start-here" in r for r in p.referenced_files)

    def test_gemini_imports_non_empty(self, project_dir: Path) -> None:
        agent_dir = project_dir / ".agent"
        generate_adapters_for_tools(project_dir, agent_dir, ["gemini"])
        hybrid = HybridParser()
        parsed_list = hybrid.parse_tool(project_dir, "gemini")
        p = parsed_list[0]
        assert len(p.imports) >= 1
        assert any(".agent/" in i for i in p.imports)


class TestAllAdaptersSemanticEquivalence:
    def test_detect_after_generate(self, project_dir: Path) -> None:
        _generate_all_adapters(project_dir)
        detected = HybridParser().detect_all(project_dir)
        assert len(detected) == 4
        assert set(detected.keys()) == {"cursor", "claude", "copilot", "gemini"}

    def test_all_reference_start_here(self, project_dir: Path) -> None:
        _generate_all_adapters(project_dir)
        parsed_list = HybridParser().parse_all(project_dir)
        for p in parsed_list:
            refs = p.referenced_files
            assert any("start-here" in r for r in refs), f"{p.tool_name} missing start-here reference"

    def test_all_reference_context_or_core_rules(self, project_dir: Path) -> None:
        _generate_all_adapters(project_dir)
        parsed_list = HybridParser().parse_all(project_dir)
        for p in parsed_list:
            refs = p.referenced_files
            has_context = any("context" in r for r in refs)
            has_core = any("core-rules" in r for r in refs)
            assert has_context or has_core, f"{p.tool_name} should reference context or core-rules"

    def test_all_mention_utf8(self, project_dir: Path) -> None:
        _generate_all_adapters(project_dir)
        parsed_list = HybridParser().parse_all(project_dir)
        for p in parsed_list:
            rules_text = " ".join(p.rules).lower()
            raw_lower = p.raw_content.lower()
            assert "utf-8" in raw_lower or "utf-8" in rules_text, (
                f"{p.tool_name} should mention UTF-8"
            )
