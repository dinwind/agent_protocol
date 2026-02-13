"""
Test context building across multiple environments and compare results.

Simulates several (stack, task) scenarios as "environments", runs the protocol
context build (get_context_files + optional build_context_content), and:

- Asserts every environment gets the same essential+context base.
- Asserts stack-specific files only when that stack is requested.
- Asserts task-specific workflows/skills differ by task profile.
- Compares built content digest to ensure different envs produce different
  context (and expected snippets appear in content).

Environments used: minimal, python_coding, python_review, rust_bugfix, mixed_docs.
"""

import hashlib
import json
from pathlib import Path

import pytest

from cokodo_agent.fetcher.builtin import BuiltinFetcher
from cokodo_agent.sync import build_context_content, get_context_files


def _get_bundled_agent_dir() -> Path:
    """Path to bundled .agent used for context build tests."""
    fetcher = BuiltinFetcher()
    if not fetcher.is_available():
        pytest.skip("Bundled protocol not available")
    path, _ = fetcher.fetch()
    return path


# Environments: (id, stack, task) for reproducible scenarios
ENVIRONMENTS = [
    ("minimal", None, None),  # essential + context only
    ("python_coding", "python", "feature_development"),
    ("python_review", "python", "code_review"),
    ("rust_bugfix", "rust", "bug_fix"),
    ("mixed_docs", "mixed", "documentation"),
]


class TestContextBuildEnvironments:
    """Simulate context build for several environments and compare."""

    @pytest.fixture(scope="class")
    def agent_dir(self) -> Path:
        return _get_bundled_agent_dir()

    @pytest.fixture(scope="class")
    def manifest_layers(self, agent_dir: Path) -> dict:
        manifest_path = agent_dir / "manifest.json"
        if not manifest_path.exists():
            return {}
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return data.get("loading_strategy", {}).get("layers", {})

    def test_each_environment_returns_file_list(self, agent_dir: Path) -> None:
        """Each (stack, task) environment produces a non-empty, ordered file list."""
        for env_id, stack, task in ENVIRONMENTS:
            files = get_context_files(agent_dir, stack=stack, task=task)
            assert isinstance(files, list), f"{env_id}: expected list"
            assert len(files) > 0, f"{env_id}: expected at least essential+context"
            assert len(files) == len(set(files)), f"{env_id}: no duplicates"

    def test_common_base_identical_across_environments(self, agent_dir: Path) -> None:
        """Essential + context file set is included in every environment."""
        data = json.loads((agent_dir / "manifest.json").read_text(encoding="utf-8"))
        layers = data.get("loading_strategy", {}).get("layers", {})
        essential = layers.get("essential", {}).get("files", [])
        context = layers.get("context", {}).get("files", [])
        base_set = set(essential + context)

        for env_id, stack, task in ENVIRONMENTS:
            files = get_context_files(agent_dir, stack=stack, task=task)
            file_set = set(files)
            missing = base_set - file_set
            assert not missing, f"{env_id}: missing base files {missing}"

    def test_stack_specific_files_only_when_stack_given(
        self, agent_dir: Path, manifest_layers: dict
    ) -> None:
        """Stack-specific files appear only for environments with that stack."""
        stack_specs = manifest_layers.get("stack_specs", {}).get("options", {})
        if not stack_specs:
            pytest.skip("No stack_specs in manifest")

        minimal_files = set(get_context_files(agent_dir, stack=None, task=None))
        python_files = set(get_context_files(agent_dir, stack="python", task=None))
        rust_files = set(get_context_files(agent_dir, stack="rust", task=None))
        mixed_files = set(get_context_files(agent_dir, stack="mixed", task=None))

        python_only = stack_specs.get("python", [])
        rust_only = stack_specs.get("rust", [])
        for f in python_only:
            assert f not in minimal_files, f"minimal should not have stack file {f}"
            assert f in python_files, f"python env should include {f}"
        for f in rust_only:
            assert f not in minimal_files, f"minimal should not have stack file {f}"
            assert f in rust_files, f"rust env should include {f}"
        # mixed should have both python and rust stack files
        for f in python_only + rust_only:
            assert f in mixed_files, f"mixed env should include {f}"

    def test_task_specific_workflows_and_skills_differ(
        self, agent_dir: Path, manifest_layers: dict
    ) -> None:
        """Different tasks yield different workflow/skill file sets."""
        task_profiles = (
            (agent_dir / "manifest.json")
            .read_text(encoding="utf-8")
        )
        data = json.loads(task_profiles)
        profiles = data.get("loading_strategy", {}).get("task_profiles", {})
        if not profiles:
            pytest.skip("No task_profiles in manifest")

        minimal = set(get_context_files(agent_dir, stack=None, task=None))
        feature_dev = set(get_context_files(agent_dir, stack="python", task="feature_development"))
        code_review = set(get_context_files(agent_dir, stack="python", task="code_review"))
        documentation = set(get_context_files(agent_dir, stack=None, task="documentation"))

        # feature_development has coding + testing workflows; code_review has review + guardian
        workflows = manifest_layers.get("workflows", {}).get("mappings", {})
        coding_files = set(workflows.get("coding", []))
        review_files = set(workflows.get("review", []))
        doc_files = set(workflows.get("documentation", []))

        assert coding_files.issubset(feature_dev), "feature_development should load coding workflows"
        assert review_files.issubset(code_review), "code_review should load review workflows"
        assert doc_files.issubset(documentation), "documentation task should load doc workflows"
        # minimal has no task so no workflow files beyond what's in essential+context
        for wf in list(coding_files)[:1]:  # at least one coding file not in minimal
            if wf not in (manifest_layers.get("essential", {}).get("files", [])
                         + manifest_layers.get("context", {}).get("files", [])):
                assert wf not in minimal
                break

    def test_built_content_digest_differs_by_environment(self, agent_dir: Path) -> None:
        """Built context content (concatenated) differs when stack or task differs."""
        digests = {}
        for env_id, stack, task in ENVIRONMENTS:
            files = get_context_files(agent_dir, stack=stack, task=task)
            content_map = build_context_content(agent_dir, files)
            # Deterministic concatenation for digest
            ordered = "\n---\n".join(
                content_map.get(f, "") for f in files if f in content_map
            )
            digests[env_id] = hashlib.sha256(ordered.encode("utf-8")).hexdigest()

        # At least two environments should differ (e.g. minimal vs python_coding)
        assert digests["minimal"] != digests["python_coding"], (
            "minimal and python_coding should produce different context content"
        )
        assert digests["python_coding"] != digests["python_review"], (
            "different tasks should produce different context content"
        )
        assert digests["python_review"] != digests["rust_bugfix"], (
            "different stacks should produce different context content"
        )

    def test_built_content_includes_expected_snippets(self, agent_dir: Path) -> None:
        """Built content for stack/task includes expected file content."""
        files = get_context_files(agent_dir, stack="python", task="feature_development")
        content_map = build_context_content(agent_dir, files)

        # Should include start-here and core-rules
        assert "start-here.md" in content_map, "context should include start-here.md"
        assert any("core-rules" in f for f in content_map), "context should include core-rules"

        # Python stack should have python stack spec
        python_spec = "core/stack-specs/python.md"
        assert python_spec in content_map, "python env should include python stack spec"
        assert "python" in content_map[python_spec].lower(), "python spec should mention python"

        # feature_development should include bug-prevention or design-principles (coding)
        workflow_files = [f for f in content_map if "workflows" in f]
        assert len(workflow_files) >= 1, "feature_development should add workflow files"
