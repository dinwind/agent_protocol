"""Parser for Claude Code instruction files (CLAUDE.md and .claude/rules/*.md)."""

from pathlib import Path

from cokodo_agent.parser.base import BaseParser
from cokodo_agent.parser.models import DetectedFile, ParsedInstruction


class ClaudeParser(BaseParser):
    """Parse Claude Code: CLAUDE.md (current), .claude/rules/*.md, or .claude/instructions.md (legacy)."""

    tool_name = "claude"

    def detect(self, project_root: Path) -> list[DetectedFile]:
        detected: list[DetectedFile] = []
        claude_md = project_root / "CLAUDE.md"
        if claude_md.exists():
            detected.append(
                DetectedFile(
                    tool_name=self.tool_name,
                    path="CLAUDE.md",
                    format_version="current",
                )
            )
        rules_dir = project_root / ".claude" / "rules"
        if rules_dir.exists():
            for p in sorted(rules_dir.rglob("*.md")):
                try:
                    rel = p.relative_to(project_root)
                except ValueError:
                    continue
                detected.append(
                    DetectedFile(
                        tool_name=self.tool_name,
                        path=str(rel).replace("\\", "/"),
                        format_version="current",
                    )
                )
        if not detected:
            legacy = project_root / ".claude" / "instructions.md"
            if legacy.exists():
                detected.append(
                    DetectedFile(
                        tool_name=self.tool_name,
                        path=".claude/instructions.md",
                        format_version="legacy",
                    )
                )
        return detected

    def parse_file(
        self, file_path: Path, project_root: Path | None = None
    ) -> ParsedInstruction:
        content = file_path.read_text(encoding="utf-8")
        root = project_root or file_path.parent
        try:
            rel_path = str(file_path.relative_to(root)).replace("\\", "/")
        except ValueError:
            rel_path = str(file_path)

        frontmatter, body = self._extract_frontmatter(content)
        format_version = "legacy" if ".claude/instructions.md" in rel_path else "current"

        return ParsedInstruction(
            tool_name=self.tool_name,
            format_version=format_version,
            ide_spec_version=self._get_spec_version(),
            source_path=rel_path,
            raw_content=content,
            frontmatter=frontmatter,
            project_name=self._extract_project_name(body),
            referenced_files=self._extract_agent_references(content),
            imports=[],
            rules=self._extract_rules(body),
            sections=self._extract_sections(body),
        )
