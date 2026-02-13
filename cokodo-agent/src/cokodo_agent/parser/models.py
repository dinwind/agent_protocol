"""Data models for IDE instruction file parsing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DetectedFile:
    """A detected IDE instruction file."""

    tool_name: str  # "cursor" | "claude" | "copilot" | "gemini"
    path: str  # path relative to project root or absolute
    format_version: str  # "current" | "legacy"


@dataclass
class ParsedInstruction:
    """Unified result of parsing one IDE instruction file."""

    tool_name: str  # "cursor" | "claude" | "copilot" | "gemini"
    format_version: str  # "current" | "legacy"
    ide_spec_version: str  # Parser target spec version (from config.IDE_SPEC_VERSIONS)
    source_path: str  # path of the parsed file
    raw_content: str  # full raw text
    frontmatter: dict[str, Any]  # YAML frontmatter (empty if none)
    project_name: str | None  # extracted from H1 or frontmatter
    referenced_files: list[str]  # all .agent/ path references
    imports: list[str]  # @import lines (Gemini only)
    rules: list[str]  # extracted rule bullet items
    sections: dict[str, str]  # {heading: body_text}
