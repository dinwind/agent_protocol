"""Base parser and shared extraction helpers for IDE instruction files."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from cokodo_agent.parser.models import DetectedFile, ParsedInstruction


def _parse_simple_frontmatter(block: str) -> dict[str, Any]:
    """Parse YAML-like frontmatter with simple key: value (no nested structures)."""
    result: dict[str, Any] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            value = int(value)
        result[key] = value
    return result


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Split content into frontmatter dict and body. Returns (frontmatter, body)."""
    if not content.strip().startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    frontmatter = _parse_simple_frontmatter(parts[1])
    body = parts[2].lstrip("\n")
    return frontmatter, body


def extract_agent_references(content: str) -> list[str]:
    """Extract all .agent/ path references from text."""
    pattern = r"\.agent/[\w/.-]+"
    found = re.findall(pattern, content)
    return list(dict.fromkeys(found))  # preserve order, dedupe


def extract_sections(content: str) -> dict[str, str]:
    """Split Markdown by ## headings; return {heading: body}."""
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_body: list[str] = []
    for line in content.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_body).strip()
            current_heading = line[3:].strip()
            current_body = []
        elif current_heading is not None:
            current_body.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_body).strip()
    return sections


def extract_rules(content: str) -> list[str]:
    """Extract bullet rule items from Key Rules / Rules / Standards sections."""
    sections = extract_sections(content)
    rules: list[str] = []
    for name in ("Key Rules", "Rules", "Standards", "Coding Standards"):
        body = sections.get(name, "")
        if not body:
            continue
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("- ") and len(line) > 2:
                rules.append(line[2:].strip())
    return rules


def extract_project_name(content: str) -> str | None:
    """Extract project name from first # heading."""
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("# ") and len(s) > 2:
            return s[2:].strip()
    return None


def extract_imports(content: str) -> list[str]:
    """Extract @path lines (Gemini import syntax)."""
    imports: list[str] = []
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("@") and len(s) > 1:
            imports.append(s)
    return imports


def get_ide_spec_version(tool_name: str) -> str:
    """Return the parser target spec version for the given IDE (from config)."""
    try:
        from cokodo_agent.config import IDE_SPEC_VERSIONS
        info = IDE_SPEC_VERSIONS.get(tool_name, {})
        return info.get("spec_version", "unknown")
    except Exception:
        return "unknown"


class BaseParser(ABC):
    """Abstract base for per-IDE instruction file parsers."""

    tool_name: str = ""

    def _get_spec_version(self) -> str:
        return get_ide_spec_version(self.tool_name)

    @abstractmethod
    def detect(self, project_root: Path) -> list[DetectedFile]:
        """Return list of detected instruction files for this IDE."""
        ...

    @abstractmethod
    def parse_file(self, file_path: Path, project_root: Path | None = None) -> ParsedInstruction:
        """Parse a single file and return ParsedInstruction."""
        ...

    def _extract_frontmatter(self, content: str) -> tuple[dict[str, Any], str]:
        return extract_frontmatter(content)

    def _extract_agent_references(self, content: str) -> list[str]:
        return extract_agent_references(content)

    def _extract_rules(self, content: str) -> list[str]:
        return extract_rules(content)

    def _extract_sections(self, content: str) -> dict[str, str]:
        return extract_sections(content)

    def _extract_project_name(self, content: str) -> str | None:
        return extract_project_name(content)

    def _extract_imports(self, content: str) -> list[str]:
        return extract_imports(content)
