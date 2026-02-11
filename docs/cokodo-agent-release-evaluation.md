# Cokodo-Agent 发布评估报告

> 评估日期：2026-02-11  
> 目标：评估开发状态、清理后发布新版本

---

## 1. 版本与一致性

| 位置 | 当前值 | 说明 |
|------|--------|------|
| `cokodo-agent/pyproject.toml` | **1.3.0** | 包版本（发布源） |
| `cokodo-agent/src/cokodo_agent/config.py` | **1.3.0** | CLI 显示用 VERSION ✓ |
| `cokodo-agent/src/cokodo_agent/__init__.py` | **1.0.0** | ❌ 与 pyproject 不一致，需改为 1.3.0 |
| `cokodo-agent/README.md` 示例输出 | **v1.2.0** | ❌ 需改为 v1.3.0 |

**结论**：发布前必须统一为 **1.3.0**（修正 `__init__.py` 与 README 示例）。

---

## 2. 测试与质量

| 项目 | 状态 |
|------|------|
| 测试 | 79 个用例全部通过 |
| 覆盖率 | 约 70%（cli/generator 部分分支未覆盖，可接受） |
| 运行环境 | Python 3.13.7 下通过（pyproject 要求 >=3.9） |

**结论**：测试健康，可直接作为发布前检查依据。

---

## 3. 仓库与构建

| 项目 | 状态 |
|------|------|
| CI 发布 | 根目录 `.github/workflows/release.yml`：`push` 标签 `v*` 触发；`working-directory: cokodo-agent` |
| 构建 | hatchling，`python -m build` 正常 |
| 产物 | wheel + sdist，路径 `cokodo-agent/dist/` |

**结论**：打 tag（如 `v1.3.0`）即可触发 PyPI 发布与 GitHub Release。

---

## 4. 待清理项

| 项 | 建议 |
|----|------|
| `cokodo-agent/.coverage` | 未跟踪，建议加入 `.gitignore`（根或 cokodo-agent），避免误提交 |
| 版本三处一致 | 见第 1 节，修正 `__init__.py` 与 README |

---

## 5. 可选改进（非阻塞发布）

- 无 CHANGELOG：若希望版本历史可读，可新增 `CHANGELOG.md` 或依赖 GitHub Release 自动生成说明。
- 覆盖率：`fetcher/github.py`、`fetcher/remote.py`、`prompts.py` 覆盖率较低，多为网络/交互分支，可后续补测。

---

## 6. 发布前检查清单

- [ ] 将 `src/cokodo_agent/__init__.py` 中 `__version__` 改为 `"1.3.0"`
- [ ] 将 README 中示例版本由 `v1.2.0` 改为 `v1.3.0`
- [ ] 在根 `.gitignore` 或 `cokodo-agent/.gitignore` 中加入 `.coverage`
- [ ] 在仓库根目录执行：`cd cokodo-agent && pytest -v`
- [ ] 确认 `pyproject.toml` 版本为 1.3.0，无需再改
- [ ] 提交上述修改后打 tag：`git tag v1.3.0`，推送：`git push origin v1.3.0`
- [ ] 在 GitHub 查看 Actions 是否完成 PyPI 发布与 Release 创建

---

## 7. 总结

| 维度 | 评估 |
|------|------|
| 功能与测试 | 就绪，可发布 |
| 版本一致性 | 需小改 2 处（__init__.py、README） |
| 仓库/CI | 就绪 |
| 清理 | 建议加入 .coverage 到 .gitignore |

完成上述 3 项修改（版本 x2 + .gitignore）并通过测试后，即可打 tag 发布 **v1.3.0**。
