# Create Agent Protocol

A CLI tool to generate standardized AI collaboration protocol (`.agent`) for your projects.

Similar to `create-react-app`, this tool helps you quickly set up an `.agent` directory with best practices for AI-assisted development.

---

## Installation

```bash
# Install globally
pip install create-agent-protocol

# Or use pipx (recommended)
pipx install create-agent-protocol
```

---

## Quick Start

```bash
# Navigate to your project
cd my-project

# Run the generator
cap init

# Or specify a path
cap init ./new-project
```

---

## Usage

### Interactive Mode (Default)

```bash
$ cap init

  Create Agent Protocol v1.0.0
  ============================

  Fetching protocol...
    [1/2] GitHub Release... OK (v2.1.0)

? Project name: my-awesome-app
? Brief description: A task management web application

? Primary tech stack:
  > Python
    Rust
    Qt/C++
    Mixed
    Other

? AI tools to configure: (space to select)
  [x] Cursor
  [x] GitHub Copilot
  [ ] Claude Projects

  Generating .agent/
  [========================================] 100%

  Success! Created .agent in /path/to/my-awesome-app

  Next steps:
    1. Review .agent/project/context.md
    2. Start coding with AI assistance!
```

### Quick Mode

```bash
# Use defaults, skip prompts
cap init --yes

# Specify options directly
cap init --name "my-app" --stack python
```

### Commands

| Command | Description |
|---------|-------------|
| `cap init [path]` | Create .agent in target directory |
| `cap version` | Show version information |

### Options

| Option | Description |
|--------|-------------|
| `--yes, -y` | Skip prompts, use defaults |
| `--name` | Project name |
| `--stack` | Tech stack (python/rust/qt/mixed/other) |
| `--force` | Overwrite existing .agent directory |
| `--offline` | Use built-in protocol (no network) |

---

## Protocol Sources

The tool fetches the latest protocol from multiple sources with fallback:

| Priority | Source | Description |
|----------|--------|-------------|
| 1 | GitHub Release | Latest version from repository |
| 2 | Remote Server | Backup server [reserved] |
| 3 | Built-in | Bundled version in package |

```
Priority 1: GitHub Release
    |
    | [unavailable]
    v
Priority 2: Remote Server [reserved, not implemented]
    |
    | [unavailable]
    v
Priority 3: Built-in (offline fallback)
```

---

## Generated Structure

```
your-project/
+-- .agent/                     # Protocol directory
|   +-- start-here.md           # * Entry point
|   +-- quick-reference.md      # Cheat sheet
|   +-- index.md                # Navigation
|   +-- manifest.json           # Config
|   +-- core/                   # Governance rules
|   +-- project/                # Project-specific
|   |   +-- context.md          # <- Customized
|   |   +-- tech-stack.md       # <- Customized
|   +-- skills/                 # Skill modules
|   +-- adapters/               # Tool adapters
|   +-- meta/                   # Protocol evolution
|   +-- scripts/                # Helper scripts
|
+-- .cursorrules                # [Optional] Cursor config
+-- .github/
    +-- copilot-instructions.md # [Optional] Copilot config
```

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CAP_OFFLINE` | Force offline mode (`1` or `true`) |
| `CAP_CACHE_DIR` | Custom cache directory |

### Cache Location

Downloaded protocols are cached at:
- Linux/macOS: `~/.cache/cap/`
- Windows: `%LOCALAPPDATA%\cap\cache\`

---

## Development

```bash
# Clone repository
git clone https://github.com/dinwind/agent_protocol.git
cd agent_protocol/create-agent-protocol

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Links

- [Agent Protocol Documentation](https://github.com/dinwind/agent_protocol)
- [Report Issues](https://github.com/dinwind/agent_protocol/issues)
