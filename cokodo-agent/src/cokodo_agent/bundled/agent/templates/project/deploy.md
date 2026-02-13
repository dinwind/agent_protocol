# Deployment

> **Instance file**: This file contains project-specific deployment information.

---

## Environments

| Environment | URL / Host | Purpose |
|-------------|-----------|---------|
| Development | `localhost:[PORT]` | Local development |
| Staging | [host] | Pre-production testing |
| Production | [host] | Live service |

---

## Deployment Commands

### Build for Production

```bash
[command]
```

### Deploy

```bash
[command]
```

### Rollback

```bash
[command]
```

---

## Verification Checklist

After each deployment, complete the following checks:

- [ ] Application starts without errors
- [ ] Health check endpoint responds (if applicable)
- [ ] Core user flow works (smoke test)
- [ ] No new errors in logs
- [ ] Performance is within acceptable range

### Smoke Test Script (if available)

```bash
[command or script path]
```

---

## Infrastructure

### Services

| Service | Technology | Port | Notes |
|---------|-----------|------|-------|
| [Service 1] | [Tech] | [Port] | [Notes] |

### Configuration Files

| File | Purpose |
|------|---------|
| [config file] | [Purpose] |

---

## Access Information

| Item | Value |
|------|-------|
| SSH | `[user@host]` |
| Deploy Path | `[path]` |
| Log Path | `[path]` |

> **Security Note**: Do not store credentials in this file. Use environment variables or secret management.

---

## Troubleshooting

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| [Symptom] | [Cause] | [Fix] |

---

*Last updated: [DATE]*
