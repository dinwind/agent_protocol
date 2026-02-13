"""Configuration constants."""

import os
from pathlib import Path
from typing import TypedDict


class AIToolInfo(TypedDict):
    """Type definition for AI tool configuration."""

    name: str
    file: str | None
    template: str | None


class IDESpecVersion(TypedDict):
    """Version and doc reference for an IDE's instruction format (parser/generator target)."""

    spec_version: str  # Parser/generator target, e.g. "2026-02" or vendor version
    spec_date: str  # Date last validated (YYYY-MM-DD)
    doc_url: str  # Official doc URL for the format


# Version
VERSION = "1.3.1"
BUNDLED_PROTOCOL_VERSION = "3.1.1"

# GitHub Release
GITHUB_REPO = "dinwind/agent_protocol"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_DOWNLOAD_URL = f"https://github.com/{GITHUB_REPO}/releases/download"

# Remote Server (reserved for future)
REMOTE_SERVER_URL = os.environ.get("COKODO_REMOTE_SERVER", "")

# Cache
DEFAULT_CACHE_DIR = Path(
    os.environ.get(
        "COKODO_CACHE_DIR",
        (
            Path.home() / ".cache" / "cokodo"
            if os.name != "nt"
            else Path(os.environ.get("LOCALAPPDATA", Path.home())) / "cokodo" / "cache"
        ),
    )
)

# Offline mode
OFFLINE_MODE = os.environ.get("COKODO_OFFLINE", "").lower() in ("1", "true", "yes")

# Tech stacks
TECH_STACKS = {
    "python": "Python",
    "rust": "Rust",
    "qt": "Qt/C++",
    "mixed": "Mixed (Python + Rust)",
    "other": "Other",
}

# AI Tools
AI_TOOLS: dict[str, AIToolInfo] = {
    "cokodo": {
        "name": "Cokodo (Protocol Only)",
        "file": None,  # No additional file, just .agent/
        "template": None,
    },
    "cursor": {
        "name": "Cursor",
        "file": ".cursor/rules/",  # Directory: generates .mdc files with YAML frontmatter
        "template": None,
    },
    "copilot": {
        "name": "GitHub Copilot",
        "file": "AGENTS.md",  # Project root; recognized by Copilot agent mode
        "template": None,
    },
    "claude": {
        "name": "Claude Code",
        "file": "CLAUDE.md",  # Project root; auto-loaded every session
        "template": None,
    },
    "gemini": {
        "name": "Gemini Code Assist",
        "file": "GEMINI.md",  # Project root; supports @file.md import syntax
        "template": None,
    },
}

# Legacy (deprecated) file paths per IDE — for parser/import compatibility
LEGACY_TOOL_FILES: dict[str, list[str]] = {
    "cursor": [".cursorrules"],
    "claude": [".claude/instructions.md"],
    "copilot": [".github/copilot-instructions.md"],
    "gemini": [".agent/rules/"],  # directory of .md files
}

# Third-party IDE spec versions (parser/generator target; update when vendors change format)
IDE_SPEC_VERSIONS: dict[str, IDESpecVersion] = {
    "cursor": {
        "spec_version": "2026-02",
        "spec_date": "2026-02-13",
        "doc_url": "https://docs.cursor.com/context/rules",
    },
    "claude": {
        "spec_version": "2026-02",
        "spec_date": "2026-02-13",
        "doc_url": "https://www.claude.com/blog/using-claude-md-files",
    },
    "copilot": {
        "spec_version": "2026-02",
        "spec_date": "2026-02-13",
        "doc_url": "https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions",
    },
    "gemini": {
        "spec_version": "2026-02",
        "spec_date": "2026-02-13",
        "doc_url": "https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html",
    },
}
