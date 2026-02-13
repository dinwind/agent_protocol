"""Parser for Gemini Code Assist instruction files (GEMINI.md and .agent/rules/)."""

from pathlib import Path

from cokodo_agent.parser.base import BaseParser
from cokodo_agent.parser.models import DetectedFile, ParsedInstruction

MAX_IMPORT_DEPTH = 5


class GeminiParser(BaseParser):
    """Parse Gemini: GEMINI.md (current) or .agent/rules/*.md (legacy Antigravity)."""

    tool_name = "gemini"

    def detect(self, project_root: Path) -> list[DetectedFile]:
        detected: list[DetectedFile] = []
        gemini_md = project_root / "GEMINI.md"
        if gemini_md.exists():
            detected.append(
                DetectedFile(
                    tool_name=self.tool_name,
                    path="GEMINI.md",
                    format_version="current",
                )
            )
        if not detected:
            rules_dir = project_root / ".agent" / "rules"
            if rules_dir.exists():
                for p in sorted(rules_dir.glob("*.md")):
                    if p.name.upper() == "README.MD":
                        continue
                    try:
                        rel = p.relative_to(project_root)
                    except ValueError:
                        continue
                    detected.append(
                        DetectedFile(
                            tool_name=self.tool_name,
                            path=str(rel).replace("\\", "/"),
                            format_version="legacy",
                        )
                    )
        return detected

    def parse_file(
        self, file_path: Path, project_root: Path | None = None
    ) -> ParsedInstruction:
        root = project_root or file_path.parent
        content = file_path.read_text(encoding="utf-8")
        try:
            rel_path = str(file_path.relative_to(root)).replace("\\", "/")
        except ValueError:
            rel_path = str(file_path)

        format_version = (
            "legacy"
            if rel_path.startswith(".agent/rules/")
            else "current"
        )

        imports = self._extract_imports(content)
        referenced = list(self._extract_agent_references(content))
        for imp in imports:
            path_str = imp[1:].strip()  # drop @
            if path_str not in referenced:
                referenced.append(path_str)

        if format_version == "current" and imports and root:
            expanded_refs = self._resolve_imports(root, content, seen={})
            for r in expanded_refs:
                if r not in referenced:
                    referenced.append(r)

        return ParsedInstruction(
            tool_name=self.tool_name,
            format_version=format_version,
            ide_spec_version=self._get_spec_version(),
            source_path=rel_path,
            raw_content=content,
            frontmatter={},
            project_name=self._extract_project_name(content),
            referenced_files=referenced,
            imports=imports,
            rules=self._extract_rules(content),
            sections=self._extract_sections(content),
        )

    def _resolve_imports(
        self,
        project_root: Path,
        content: str,
        depth: int = 0,
        seen: set[str] | None = None,
    ) -> list[str]:
        if depth >= MAX_IMPORT_DEPTH:
            return []
        seen = seen or set()
        refs: list[str] = []
        for line in content.splitlines():
            s = line.strip()
            if not s.startswith("@") or len(s) <= 1:
                continue
            path_str = s[1:].strip()
            if path_str in seen:
                continue
            seen.add(path_str)
            refs.append(path_str)
            target = project_root / path_str
            if target.exists() and target.is_file():
                try:
                    sub = target.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue
                refs.extend(
                    self._resolve_imports(project_root, sub, depth + 1, seen)
                )
        return refs
