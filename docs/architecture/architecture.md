# QA Framework Architecture

## gTAA Alignment

The framework maps to the ISTQB generic Test Automation Architecture:

| gTAA Layer | Framework Implementation |
| --- | --- |
| Test Generation | `@playwright/mcp` and AI agent governance in Phase 4 |
| Test Definition | pytest tests, Journey runner, BDD-style scenario data |
| Test Execution | pytest, Playwright, Allure, Azure Pipelines |
| Test Adaptation | `BasePage`, `BaseService`, wait utilities, logging |

## Three-Layer Code Model

Test scripts never import directly from Core Libraries. They work through Business Logic layer objects.

| Layer | Folders | Responsibility |
| --- | --- | --- |
| Test Scripts | `tests/` | Test intent, marks, parametrization, assertions |
| Business Logic | `business/` | Page objects, service objects, actors, flows |
| Core Libraries | `core/` | Config, base classes, logging, data loading, journey orchestration |

## N-Tier Stack

| Tier | Implementation |
| --- | --- |
| AI Layer | `CLAUDE.md`, `package.json`, AI quality gate |
| Logic Layer | `business/actors/`, `core/journey_runner.py` |
| Page Object Layer | `business/pages/`, `core/base_page.py` |
| Service Layer | `business/services/`, `core/base_service.py` |
| Data Layer | `data/yaml/`, `data/excel/`, `core/data_loader.py` |
| Config Layer | `config/envs/`, `core/config.py` |

## Test Data Strategy

YAML and JSON are the runtime source of truth. Excel is allowed only as an import-time adapter for stakeholders who maintain spreadsheet data. Runtime tests must not import pandas directly.

## Environment Isolation

Each test worker receives an isolated schema name through the `worker_schema` fixture. The current scaffold uses an in-memory fake DB adapter so the isolation contract can be verified without a live database. Real DB creation and teardown should be wired behind the same fixture boundary.

