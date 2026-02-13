# Skill Module Interface Specification

> Defines standard structure, interface, and lifecycle for skill modules.

---

## 1. Overview

Skills are reusable capability modules in the `.agent` protocol, encapsulating domain-specific knowledge and automation scripts.

### Design Principles

| Principle | Description |
|-----------|-------------|
| **Single Responsibility** | Each skill focuses on one domain |
| **Self-Contained** | All docs, scripts, rules within directory |
| **Discoverable** | Metadata declared via manifest.json |
| **Loosely Coupled** | No strong dependencies between skills |

---

## 2. Directory Structure

```
skills/
└── {skill-name}/
    ├── SKILL.md           # Main doc (required, uppercase)
    ├── manifest.json      # Metadata (recommended)
    ├── rules/             # Rule definitions (optional)
    ├── scripts/           # Automation scripts (optional)
    └── templates/         # Template files (optional)
```

> **Note**: Entry file must be `SKILL.md` (uppercase) for [agentskills.io](https://agentskills.io) compatibility.

---

## 3. Manifest Specification

```json
{
  "name": "guardian",
  "version": "1.0.0",
  "description": "Code quality and security check skill",
  
  "triggers": {
    "explicit": ["check code", "review", "validate"],
    "automatic": ["pre-commit", "pull-request"]
  },
  
  "capabilities": [
    {
      "name": "banned-pattern-check",
      "description": "Check for forbidden code patterns"
    }
  ],
  
  "entry_points": {
    "main": "SKILL.md",
    "check": "scripts/check_all.py"
  },
  
  "tags": ["quality", "security", "automation"]
}
```

---

## 4. Skill Lifecycle

```
Discovery → Activation → Execution → Deactivation
```

**Progressive Disclosure**:
1. **Level 1**: Load YAML frontmatter (~100 tokens/skill)
2. **Level 2**: Load SKILL.md body on trigger (<5k tokens)
3. **Level 3**: Load additional files on demand (unlimited)

---

## 5. Capability Interface

### Input/Output

```python
# Standard input
SkillInput = {
    "capability": str,
    "params": dict,
    "context": {
        "project_root": str,
        "tech_stack": list,
    }
}

# Standard output
SkillOutput = {
    "success": bool,
    "results": list | dict,
    "errors": list,
    "warnings": list,
}
```

---

## 6. Parameterized Skills (Multi-Backend Pattern)

When a skill addresses a common concern (e.g., schema comparison, migration) but the implementation varies by tech stack, use the **parameterized skill** pattern instead of forking the skill per project.

### 6.1 Design

```
skills/
└── db-schema-compare/
    ├── SKILL.md              # Unified documentation
    ├── manifest.json          # Declares supported backends
    └── scripts/
        ├── compare_schema.py  # Main entry, dispatches by backend
        ├── backends/
        │   ├── prisma.py      # Prisma-specific logic
        │   ├── sqlalchemy.py  # SQLAlchemy-specific logic
        │   └── typeorm.py     # TypeORM-specific logic
        └── base.py            # Shared interface / base class
```

### 6.2 Manifest Declaration

```json
{
  "name": "db-schema-compare",
  "version": "2.0.0",
  "description": "Compare ORM schema with actual database",
  
  "parameters": {
    "backend": {
      "type": "string",
      "required": true,
      "enum": ["prisma", "sqlalchemy", "typeorm"],
      "description": "ORM backend to use"
    },
    "connection": {
      "type": "string",
      "required": false,
      "description": "Database connection string (or use Docker auto-detect)"
    }
  },
  
  "backends": {
    "prisma": {
      "description": "Prisma schema comparison",
      "schema_path": "backend/prisma/schema.prisma"
    },
    "sqlalchemy": {
      "description": "SQLAlchemy model comparison",
      "model_path": "backend/app/models/"
    }
  }
}
```

### 6.3 When to Parameterize

| Situation | Approach |
|-----------|----------|
| Same concern, different tech stack | Parameterized skill with backends |
| Completely different concern | Separate skill |
| Minor project-specific tweak | Config override in `skills/_project/` |

### 6.4 Project-Level Override

Projects can override specific behavior without forking:

```
skills/_project/
└── db-schema-compare/
    └── config.json    # Override parameters for this project
```

```json
{
  "extends": "db-schema-compare",
  "parameters": {
    "backend": "sqlalchemy",
    "connection": "postgresql://localhost:5432/mydb"
  }
}
```

---

## 7. Best Practices

### Development Checklist

- [ ] Create `SKILL.md` with YAML frontmatter
- [ ] Create `manifest.json` (recommended)
- [ ] Scripts support CLI invocation
- [ ] Scripts output structured results
- [ ] Provide usage examples
- [ ] Complete documentation
- [ ] Consider parameterization if the skill could serve multiple tech stacks

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Skill directory | kebab-case | `code-guardian` |
| Script file | snake_case | `check_all.py` |
| Rule ID | kebab-case | `no-bare-except` |
| Capability name | kebab-case | `banned-pattern-check` |

---

*This file is the skill module interface specification*
*Protocol version: 3.1.0*
