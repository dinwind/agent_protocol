# Cokodo Agent Usage Guide

> Complete guide for setting up AI collaboration protocol in your projects

[![CLI Version](https://img.shields.io/badge/CLI-v1.0.0-blue.svg)](../cokodo-agent)
[![Protocol Version](https://img.shields.io/badge/Protocol-v2.1.0-green.svg)](../.agent/manifest.json)

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [Generated Structure](#generated-structure)
- [Configuration Options](#configuration-options)
- [Post-Initialization Setup](#post-initialization-setup)
- [AI Session Templates](#ai-session-templates)
- [Common Operations](#common-operations)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Protocol Upgrade](#protocol-upgrade)

---

## Installation

### Using pip

```bash
pip install cokodo-agent
```

### Using pipx (Recommended)

```bash
pipx install cokodo-agent
```

### Verify Installation

```bash
cokodo version
```

---

## Quick Start

### Interactive Mode (Default)

```bash
# Navigate to your project
cd my-project

# Run the generator
cokodo init
```

The CLI will guide you through:

```
╭─────────────────────────╮
│  Cokodo Agent v1.0.0    │
╰─────────────────────────╯

Fetching protocol...
  OK Protocol v2.1.0

? Project name: my-awesome-app
? Brief description: A task management application
? Primary tech stack: Python
? AI tools to configure: [x] Cursor  [x] GitHub Copilot

Generating .agent/
  OK Created .agent/

╭─────────────────────────────────────────────────╮
│ Success! Created .agent in /path/to/my-project  │
│                                                 │
│ Next steps:                                     │
│   1. Review .agent/project/context.md           │
│   2. Customize .agent/project/tech-stack.md     │
│   3. Start coding with AI assistance!           │
╰─────────────────────────────────────────────────╯
```

### Quick Mode (Non-Interactive)

```bash
# Use all defaults
cokodo init --yes

# Specify project name and tech stack
cokodo init --name "MyApp" --stack python --yes

# Initialize in a specific directory
cokodo init ./new-project --yes
```

---

## Command Reference

### `cokodo init [PATH]`

Create `.agent` protocol directory in the target location.

**Arguments:**

| Argument | Description | Default |
|----------|-------------|---------|
| `PATH` | Target directory | Current directory |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--yes` | `-y` | Skip interactive prompts, use defaults |
| `--name` | `-n` | Project name |
| `--stack` | `-s` | Tech stack (`python`/`rust`/`qt`/`mixed`/`other`) |
| `--force` | `-f` | Overwrite existing `.agent` directory |
| `--offline` | | Use built-in protocol (no network) |

**Examples:**

```bash
# Interactive initialization
cokodo init

# Quick initialization with defaults
cokodo init -y

# Specify all options
cokodo init ./my-project -n "My Project" -s python -y

# Force overwrite existing protocol
cokodo init --force

# Offline mode (use bundled protocol)
cokodo init --offline
```

### `cokodo version`

Display version information for CLI and bundled protocol.

```bash
$ cokodo version
cokodo-agent v1.0.0

Protocol versions:
  Built-in: v2.1.0
```

---

## Generated Structure

After running `cokodo init`, the following structure is created:

```
your-project/
├── .agent/                         # Protocol directory
│   ├── start-here.md              # ⭐ AI entry point (read first)
│   ├── quick-reference.md         # 📋 One-page cheat sheet
│   ├── index.md                   # 🗂️ Navigation index
│   ├── manifest.json              # ⚙️ Loading strategy & metadata
│   │
│   ├── core/                      # 🔧 Governance engine (reusable)
│   │   ├── core-rules.md          #    Core philosophy & iron rules
│   │   ├── instructions.md        #    AI collaboration guidelines
│   │   ├── conventions.md         #    Naming & Git conventions
│   │   ├── security.md            #    Security development standards
│   │   ├── examples.md            #    Code examples
│   │   ├── workflows/             #    Workflow specifications
│   │   │   ├── ai-boundaries.md
│   │   │   ├── bug-prevention.md
│   │   │   ├── design-principles.md
│   │   │   ├── documentation.md
│   │   │   ├── pre-task-checklist.md
│   │   │   ├── quality-assurance.md
│   │   │   ├── review-process.md
│   │   │   └── testing.md
│   │   └── stack-specs/           #    Tech stack specifications
│   │       ├── git.md
│   │       ├── python.md
│   │       ├── rust.md
│   │       └── qt.md
│   │
│   ├── project/                   # 📋 Project instance (customized)
│   │   ├── context.md             #    ✏️ Business context
│   │   ├── tech-stack.md          #    ✏️ Technology configuration
│   │   ├── known-issues.md        #    Known issues database
│   │   └── adr/                   #    Architecture Decision Records
│   │       └── readme.md
│   │
│   ├── skills/                    # 🛠️ Skill modules
│   │   ├── skill-interface.md     #    Skill development guide
│   │   ├── guardian/              #    Code quality gate
│   │   ├── ai-integration/        #    AI service integration
│   │   └── agent-governance/      #    Protocol health check
│   │
│   ├── adapters/                  # 🔌 Tool adapters (templates)
│   │   ├── cursor/
│   │   ├── github-copilot/
│   │   ├── claude/
│   │   └── google-antigravity/
│   │
│   ├── meta/                      # 📚 Protocol evolution
│   │   ├── protocol-adr.md
│   │   └── adr-archive.md
│   │
│   └── scripts/                   # 🔧 Helper scripts
│       ├── init_agent.py
│       ├── lint-protocol.py
│       └── token-counter.py
│
├── .cursorrules                   # [Optional] Cursor configuration
├── .github/
│   └── copilot-instructions.md    # [Optional] Copilot configuration
└── .claude/
    └── instructions.md            # [Optional] Claude configuration
```

### Directory Types

| Type | Directory | Purpose | Portability |
|------|-----------|---------|-------------|
| **Engine** | `core/` | Universal governance rules | ✅ Reusable across projects |
| **Instance** | `project/` | Project-specific information | ❌ Project-exclusive |

**Core Rule:** Engine files must never contain project-specific names, paths, or business logic.

---

## Configuration Options

### Tech Stack Options

| Value | Description | Recommended Tools |
|-------|-------------|-------------------|
| `python` | Python projects | uv/pip, ruff, pytest, mypy |
| `rust` | Rust projects | cargo, clippy, rustfmt |
| `qt` | Qt/C++ projects | CMake/qmake, Qt Creator |
| `mixed` | Python + Rust | Combined tooling |
| `other` | Other stacks | Custom configuration |

### AI Tool Configurations

| Tool | Config File | Description |
|------|-------------|-------------|
| Cursor | `.cursorrules` | Cursor IDE rules |
| GitHub Copilot | `.github/copilot-instructions.md` | Copilot instructions |
| Claude | `.claude/instructions.md` | Claude project instructions |

---

## Post-Initialization Setup

### Step 1: Configure Project Context

Edit `.agent/project/context.md`:

```markdown
# Project Context

## Project Name

YourProjectName

## Description

Brief description of what this project does and what problems it solves.

## Current Status

[Development stage, MVP, Production, etc.]

## Key Features

1. Feature A - Description
2. Feature B - Description
3. Feature C - Description

## Business Rules

- Rule 1: Description
- Rule 2: Description
```

### Step 2: Configure Tech Stack

Edit `.agent/project/tech-stack.md`:

```markdown
# Tech Stack

## Primary Stack

Python

## Language Versions

- Python 3.11+
- Node.js 18+ (if applicable)

## Key Dependencies

- FastAPI 0.100+
- SQLAlchemy 2.0+
- Pydantic 2.0+

## Development Environment

- OS: Windows/Linux/macOS
- IDE: Cursor / VS Code
- Package Manager: uv / pip

## Build Commands

pip install -r requirements.txt
pytest tests/
```

### Step 3: Configure AI Tools (Optional)

If you need to customize AI tool configurations beyond the generated defaults:

| AI Tool | Action |
|---------|--------|
| **Cursor** | Edit `.cursorrules` or copy from `.agent/adapters/cursor/rules.template.md` |
| **GitHub Copilot** | Edit `.github/copilot-instructions.md` |
| **Claude** | Run `python .agent/adapters/claude/adapt_for_claude.py` |

---

## AI Session Templates

### Quick Start (Daily Use)

```
Please read .agent/start-here.md first to establish project context, 
then strictly follow the protocol rules.

Today's task: [Describe your task]
```

### Full Context (First Session or Complex Tasks)

```
Please read the following files in order to establish project context:

1. .agent/start-here.md
2. .agent/project/context.md
3. .agent/project/tech-stack.md
4. .agent/core/instructions.md
5. .agent/core/stack-specs/python.md  # Choose based on tech stack

Then proceed with today's task: [Describe your task]
```

### Debug Session

```
Please read .agent/start-here.md and .agent/core/workflows/bug-prevention.md 
to understand known issues.

I'm experiencing this bug: [Describe the issue]
```

---

## Common Operations

### Check Protocol Health

```bash
python .agent/scripts/lint-protocol.py
```

### Count Token Usage

```bash
python .agent/scripts/token-counter.py
```

### Record Bug Prevention Knowledge

Edit `.agent/core/workflows/bug-prevention.md` to add new entries:

```markdown
### Issue: [Brief Description]

**Symptom:** What happened
**Cause:** Why it happened
**Solution:** How to fix/prevent it
**Date:** YYYY-MM-DD
```

### Record Architecture Decisions

Create new ADR files in `.agent/project/adr/`:

```markdown
# ADR-001: [Decision Title]

## Status
Accepted

## Context
[Why this decision was needed]

## Decision
[What was decided]

## Consequences
[Impact of the decision]
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COKODO_OFFLINE` | Force offline mode (`1`, `true`, `yes`) | Disabled |
| `COKODO_CACHE_DIR` | Custom cache directory | OS-specific |
| `COKODO_REMOTE_SERVER` | Remote protocol server URL | None (reserved) |

### Cache Locations

| OS | Default Path |
|----|--------------|
| Linux/macOS | `~/.cache/cokodo/` |
| Windows | `%LOCALAPPDATA%\cokodo\cache\` |

---

## Troubleshooting

### Q: AI is not following protocol rules?

**Solution:** Ensure the AI reads `start-here.md` at the beginning of each session.

```
Please read .agent/start-here.md first before proceeding with any task.
```

### Q: Too many files, token consumption is too high?

**Solution:** Use the layered loading strategy defined in `manifest.json`. Only load files needed for the current task.

Essential files (~3,000 tokens):
- `start-here.md`
- `quick-reference.md`

Context files (~2,000 tokens):
- `project/context.md`
- `project/tech-stack.md`

### Q: Protocol initialization failed?

**Solution:** Check these common issues:

1. **Permission denied:** Run with appropriate permissions
2. **Directory exists:** Use `--force` to overwrite
3. **Network error:** Use `--offline` for bundled protocol

```bash
# Force overwrite with offline mode
cokodo init --force --offline
```

### Q: How to use a different protocol directory name?

**Solution:** The protocol uses `$AGENT_DIR` placeholder internally. To rename:

1. Rename the directory:
   ```bash
   mv .agent .agent_custom
   ```

2. Update `manifest.json`:
   ```json
   {
     "directory_name": ".agent_custom"
   }
   ```

---

## Protocol Upgrade

### Upgrade Steps

1. **Backup current project files:**
   ```bash
   cp -r .agent/project ./project-backup
   ```

2. **Remove old protocol:**
   ```bash
   rm -rf .agent
   ```

3. **Initialize new version:**
   ```bash
   cokodo init --force
   ```

4. **Restore project files:**
   ```bash
   cp -r ./project-backup/* .agent/project/
   ```

5. **Review changes:**
   Check `.agent/meta/protocol-adr.md` for version changes.

### Version Compatibility

| CLI Version | Protocol Version | Notes |
|-------------|------------------|-------|
| 1.0.x | 2.1.0 | Current stable |

---

## Iron Rules

These rules must always be followed:

| Rule | Description |
|------|-------------|
| **UTF-8 Encoding** | Always specify `encoding='utf-8'` explicitly |
| **Forward Slash Paths** | Use `/` instead of `\` in commands |
| **Test Data Prefix** | Use `autotest_` prefix for test data |
| **kebab-case Files** | Files in `.agent/` use lowercase with hyphens |
| **SKILL.md Uppercase** | Skill entry files use uppercase (agentskills.io standard) |

---

## Further Reading

| Document | Content |
|----------|---------|
| `.agent/start-here.md` | Protocol entry point and architecture overview |
| `.agent/quick-reference.md` | One-page quick reference |
| `.agent/meta/protocol-adr.md` | Protocol evolution history |
| `.agent/skills/skill-interface.md` | How to develop new skills |

---

## Protocol Sources

The CLI fetches protocol from multiple sources with automatic fallback:

```
Priority 1: GitHub Release (latest version)
    ↓ [unavailable]
Priority 2: Remote Server (reserved for future)
    ↓ [unavailable]
Priority 3: Built-in (offline fallback)
```

---

## Support

- **Documentation:** [Agent Protocol Repository](https://github.com/dinwind/agent_protocol)
- **Issues:** [Report Issues](https://github.com/dinwind/agent_protocol/issues)
- **Discussions:** [GitHub Discussions](https://github.com/dinwind/agent_protocol/discussions)

---

<div align="center">

**Making AI collaboration more standardized, efficient, and sustainable**

*Document Version: 1.0.0 | Protocol Version: 2.1.0 | Last Updated: 2026-01-24*

</div>
