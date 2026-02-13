"""Parser for Cursor IDE instruction files (.cursor/rules/*.mdc and .cursorrules)."""

from pathlib import Path

from cokodo_agent.parser.base import BaseParser
from cokodo_agent.parser.models import DetectedFile, ParsedInstruction


class CursorParser(BaseParser):
    """Parse Cursor rules: .cursor/rules/*.mdc (current) or .cursorrules (legacy)."""

    tool_name = "cursor"

    def detect(self, project_root: Path) -> list[DetectedFile]:
        detected: list[DetectedFile] = []
        rules_dir = project_root / ".cursor" / "rules"
        if rules_dir.exists():
            for p in rules_dir.glob("*.mdc"):
                detected.append(
                    DetectedFile(
                        tool_name=self.tool_name,
                        path=str(p.relative_to(project_root)),
                        format_version="current",
                    )
                )
        if not detected:
            legacy = project_root / ".cursorrules"
            if legacy.exists():
                detected.append(
                    DetectedFile(
                        tool_name=self.tool_name,
                        path=".cursorrules",
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

        if file_path.suffix == ".mdc":
            format_version = "current"
            frontmatter, body = self._extract_frontmatter(content)
        else:
            format_version = "legacy"
            frontmatter = {}
            body = content

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
