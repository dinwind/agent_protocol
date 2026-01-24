"""Tests for generator module."""

import pytest
import tempfile
from pathlib import Path

from cokodo_agent.generator import generate_protocol
from cokodo_agent.fetcher.builtin import BuiltinFetcher


class TestGenerator:
    """Test protocol generator."""
    
    def test_generate_creates_agent_dir(self):
        """Test that generator creates .agent directory."""
        fetcher = BuiltinFetcher()
        source_path, _ = fetcher.fetch()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = Path(tmpdir)
            config = {
                "project_name": "test-project",
                "description": "A test project",
                "tech_stack": "python",
                "ai_tools": ["cursor"],
            }
            
            generate_protocol(source_path, target_path, config)
            
            agent_dir = target_path / ".agent"
            assert agent_dir.exists()
            assert (agent_dir / "start-here.md").exists()
            assert (agent_dir / "core" / "core-rules.md").exists()
    
    def test_generate_creates_adapters(self):
        """Test that generator creates adapter files."""
        fetcher = BuiltinFetcher()
        source_path, _ = fetcher.fetch()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = Path(tmpdir)
            config = {
                "project_name": "test-project",
                "description": "",
                "tech_stack": "python",
                "ai_tools": ["cursor", "copilot"],
            }
            
            generate_protocol(source_path, target_path, config)
            
            assert (target_path / ".cursorrules").exists()
            assert (target_path / ".github" / "copilot-instructions.md").exists()
    
    def test_generate_customizes_context(self):
        """Test that generator customizes context.md."""
        fetcher = BuiltinFetcher()
        source_path, _ = fetcher.fetch()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = Path(tmpdir)
            config = {
                "project_name": "My Awesome App",
                "description": "An awesome application",
                "tech_stack": "python",
                "ai_tools": [],
            }
            
            generate_protocol(source_path, target_path, config)
            
            context_file = target_path / ".agent" / "project" / "context.md"
            content = context_file.read_text(encoding="utf-8")
            
            assert "My Awesome App" in content
            assert "An awesome application" in content
