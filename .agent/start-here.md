# AI Collaboration Entry Point

> **First message for new AI sessions**: Please read this file to establish project context, then strictly follow protocol rules.

> **IMPORTANT**: Before modifying any `.agent` files, read [meta/agent-protocol-rules.md](meta/agent-protocol-rules.md) for operation constraints.

---

## Protocol Architecture Overview

This protocol uses an **Engine-Instance Separation** architecture, decoupling generic governance rules from project-specific information:

- **`core/`**: Governance engine (generic rules, no project-specific info allowed).
- **`project/`**: Instance data (project context, tech stack, known issues).
- **`skills/`**: Modular capabilities (on-demand tools and specifications).
- **`adapters/`**: AI tool adapters (Cursor, Claude, Copilot, Gemini).

**Tooling**: The cokodo-agent CLI provides `co adapt` (generate IDE entry files from `.agent/`), `co detect` (detect existing IDE instruction files in the project), and `co import` (import from those files into `project/`). See the [usage guide](https://github.com/dinwind/agent_protocol/blob/main/docs/usage-guide_cn.md) for details. When using an IDE, prefer only this repository's `.cursor/rules` and `.agent` for project context; avoid mixing in user/global IDE rules for project-specific conventions.

---

## Context Building Path (Required Reading)

**Mandatory**: AI must load documents in the following order during first session to establish baseline understanding.

### 1. Project Context (Required for every session)

- [project/context.md](project/context.md): **Project overview** (scope, features, status).
- [project/tech-stack.md](project/tech-stack.md): **Tech stack** and environment setup.

### 2. Core Protocol (Required for every session)

- [core/core-rules.md](core/core-rules.md): **Core principles** (isolation, security, delivery quality).
- [core/conventions.md](core/conventions.md): **Naming and Git conventions**.
- [core/workflows/bug-prevention.md](core/workflows/bug-prevention.md): **Bug prevention** handbook.

### 3. Stack-Specific (Select based on project/tech-stack.md)

| Stack | File |
|-------|------|
| Python | [core/stack-specs/python.md](core/stack-specs/python.md) |
| Rust | [core/stack-specs/rust.md](core/stack-specs/rust.md) |
| Qt/C++ | [core/stack-specs/qt.md](core/stack-specs/qt.md) |

### 4. On-Demand Loading

| Scenario | File |
|----------|------|
| **Protocol operation rules** | [meta/agent-protocol-rules.md](meta/agent-protocol-rules.md) |
| **Protocol self-check** (after editing .agent) | [meta/self-check-prompt.md](meta/self-check-prompt.md) |
| Session history | [project/session-journal.md](project/session-journal.md) |
| Known issues | [project/known-issues.md](project/known-issues.md) |
| Architecture decisions | [project/adr/](project/adr/) |

---

## Design Principles

### Engine-Instance Separation
- **Engine files** (`core/`): Generic rules, project names strictly forbidden
- **Instance files** (`project/`): The only entry point for project-specific information

### Asset-Oriented Design
- `.agent` directory is a digital asset as important as source code
- Supports seamless cross-project migration
- Deletion does not affect main project operation

---

*Protocol version: 3.1.1*
