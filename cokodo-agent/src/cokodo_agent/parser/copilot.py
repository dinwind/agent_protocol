"""Parser for GitHub Copilot instruction files (AGENTS.md and .github/)."""

from pathlib import Path

from cokodo_agent.parser.base import BaseParser
from cokodo_agent.parser.models import DetectedFile, ParsedInstruction


class CopilotParser(BaseParser):
    """Parse Copilot: AGENTS.md (current), .github/copilot-instructions.md, .github/instructions/*.instructions.md."""

    tool_name = "copilot"

    def detect(self, project_root: Path) -> list[DetectedFile]:
        detected: list[DetectedFile] = []
        agents_md = project_root / "AGENTS.md"
        if agents_md.exists():
            detected.append(
                DetectedFile(
                    tool_name=self.tool_name,
                    path="AGENTS.md",
                    format_version="current",
                )
            )
        if not detected:
            repo_inst = project_root / ".github" / "copilot-instructions.md"
            if repo_inst.exists():
                detected.append(
                    DetectedFile(
                        tool_name=self.tool_name,
                        path=".github/copilot-instructions.md",
                        format_version="legacy",
                    )
                )
        if not detected:
            inst_dir = project_root / ".github" / "instructions"
            if inst_dir.exists():
                for p in sorted(inst_dir.glob("*.instructions.md")):
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
        format_version = (
            "legacy"
            if ".github/copilot-instructions.md" in rel_path
            else "current"
        )

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
