# Deployment

> **Instance file**: This file contains project-specific deployment information.
> For agent_protocol repo: this is the protocol source; no runtime deployment.

---

## Environments

| Environment | URL / Host | Purpose |
|-------------|-----------|---------|
| Development | N/A | Protocol source only; sync to downstream projects via cokodo-agent or manual copy |

---

## Deployment Commands

Not applicable. This repository is the protocol template source. Downstream projects (e.g. AuthNexus, Axlinker) use their own deploy procedures.

---

## Verification Checklist

After syncing protocol to a project:

- [ ] `co sync <project>/ --from agent_protocol` or equivalent
- [ ] Run `python .agent/scripts/lint-protocol.py` in the target project
- [ ] Confirm no required files missing

---

*Last updated: 2026-02-13*
