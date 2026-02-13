"""IDE instruction file parsers (Cursor, Claude, Copilot, Gemini)."""

from cokodo_agent.parser.hybrid import HybridParser
from cokodo_agent.parser.models import DetectedFile, ParsedInstruction

__all__ = ["HybridParser", "ParsedInstruction", "DetectedFile"]
