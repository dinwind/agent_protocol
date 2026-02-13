"""Aggregate parser for all supported IDE instruction formats."""

from pathlib import Path

from cokodo_agent.parser.claude import ClaudeParser
from cokodo_agent.parser.copilot import CopilotParser
from cokodo_agent.parser.cursor import CursorParser
from cokodo_agent.parser.gemini import GeminiParser
from cokodo_agent.parser.models import DetectedFile, ParsedInstruction


class HybridParser:
    """Detect and parse instruction files from Cursor, Claude, Copilot, and Gemini."""

    def __init__(self) -> None:
        self._parsers = [
            CursorParser(),
            ClaudeParser(),
            CopilotParser(),
            GeminiParser(),
        ]

    def detect_all(self, project_root: Path) -> dict[str, list[DetectedFile]]:
        """Return {tool_name: [detected_files]} for all tools that have files."""
        result: dict[str, list[DetectedFile]] = {}
        for parser in self._parsers:
            files = parser.detect(project_root)
            if files:
                result[parser.tool_name] = files
        return result

    def parse_all(self, project_root: Path) -> list[ParsedInstruction]:
        """Parse all detected IDE instruction files in the project."""
        result: list[ParsedInstruction] = []
        for tool_name, files in self.detect_all(project_root).items():
            parser = self._parser_for(tool_name)
            for det in files:
                path = project_root / det.path
                if path.exists():
                    result.append(parser.parse_file(path, project_root))
        return result

    def parse_tool(
        self, project_root: Path, tool: str
    ) -> list[ParsedInstruction]:
        """Parse only the given tool's instruction files."""
        parser = self._parser_for(tool)
        detected = parser.detect(project_root)
        result: list[ParsedInstruction] = []
        for det in detected:
            path = project_root / det.path
            if path.exists():
                result.append(parser.parse_file(path, project_root))
        return result

    def _parser_for(self, tool: str):
        for p in self._parsers:
            if p.tool_name == tool:
                return p
        raise ValueError(f"Unknown tool: {tool}")
