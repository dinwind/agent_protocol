# Project Conventions

> **Instance file**: Project-specific conventions. For agent_protocol repo, this documents protocol maintenance conventions.

---

## Conventions

### Convention 1: Protocol version bump

**Scope**: `manifest.json`, any file with "Protocol version" footer.

**Rule**: When adding new engine files or changing core behavior, bump minor or patch in manifest and update protocol version in affected file footers.

**Rationale**: Downstream projects need to know which protocol version they are on.

---

### Convention 2: New project templates

**Scope**: `templates/project/*.md`.

**Rule**: New standard project files must have a template in `templates/project/` and be registered in `meta/agent-protocol-rules.md` and `manifest.json`.

**Rationale**: Ensures init and sync can create a complete project structure.

---

*Last updated: 2026-02-13*
