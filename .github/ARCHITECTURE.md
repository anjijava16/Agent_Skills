# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **~200 Specialist Agents** - Role-based AI personas across all domains
- **~970 Skills** - Domain-specific knowledge modules across 40+ categories
- **20 Global Workflows** - Slash command procedures
- **53 Plugins** - Bundled multi-agent/skill packs
- **1 Rule File** - Global behavior control (GEMINI.md)

---

## 🏗️ Directory Structure

```plaintext
.github/
├── ARCHITECTURE.md          # This file
├── agents/                  # ~200 Specialist Agents
├── skills/                  # ~970 Skills
├── global_workflows/        # 20 Slash Commands
├── plugins/                 # 53 Bundled Plugin Packs
├── rules/                   # Global Rules (GEMINI.md)
└── .curos/                  # Cursor IDE configuration
```

---

## 🤖 Agents (~200)

Specialist AI personas for every domain. Agents are organized by category.

### Core Development Team

| Agent | Focus |
| ----- | ----- |
| `orchestrator` | Multi-agent coordination |
| `project-planner` | Discovery, task planning |
| `frontend-specialist` | Web UI/UX |
| `backend-specialist` | API, business logic |
| `database-architect` | Schema, SQL |
| `mobile-developer` | iOS, Android, React Native |
| `game-developer` | Game logic, mechanics |
| `devops-engineer` | CI/CD, Docker |
| `security-auditor` | Security compliance, OWASP |
| `penetration-tester` | Offensive security |
| `test-engineer` | Testing strategies |
| `debugger` | Root cause analysis |
| `performance-optimizer` | Speed, Web Vitals |
| `seo-specialist` | Ranking, visibility |
| `documentation-writer` | Manuals, docs |
| `product-manager` | Requirements, user stories |
| `product-owner` | Strategy, backlog, MVP |
| `qa-automation-engineer` | E2E testing, CI pipelines |
| `code-archaeologist` | Legacy code, refactoring |
| `explorer-agent` | Codebase analysis |

### Beast Mode / Power Agents

| Agent | Focus |
| ----- | ----- |
| `4.1-Beast` | GPT-4.1 top-tier coding |
| `Thinking-Beast-Mode` | Quantum cognitive architecture |
| `Ultimate-Transparent-Thinking-Beast-Mode` | Full transparent reasoning |
| `gpt-5-beast-mode` | GPT-5 autonomous problem solving |
| `voidbeast-gpt41enhanced` | Multi-mode developer assistant |
| `rust-gpt-4.1-beast-mode` | Rust-specialized beast mode |
| `blueprint-mode` | Structured workflow execution |

### Azure & Cloud Agents

| Agent | Focus |
| ----- | ----- |
| `arch` | Senior cloud architect |
| `azure-iac-exporter` | Export Azure resources to IaC |
| `azure-iac-generator` | Generate Bicep/ARM/Terraform/Pulumi |
| `azure-logic-apps-expert` | Logic Apps workflow design |
| `azure-policy-analyzer` | Azure Policy compliance analysis |
| `azure-principal-architect` | Azure Well-Architected guidance |
| `azure-saas-architect` | Multitenant SaaS on Azure |
| `azure-verified-modules-bicep` | AVM Bicep IaC |
| `azure-verified-modules-terraform` | AVM Terraform IaC |
| `bicep-implement` | Bicep IaC implementation |
| `bicep-plan` | Bicep IaC planning |
| `terraform` | Terraform with HCP workflows |
| `terraform-azure-implement` | Azure Terraform implementation |
| `terraform-azure-planning` | Azure Terraform planning |
| `terraform-iac-reviewer` | Terraform safety reviews |
| `arm-migration` | x86 to Arm workload migration |
| `kusto-assistant` | KQL for Azure Data Explorer |
| `terratest-module-testing` | Go Terratest suites |

### MCP Server Development Agents

| Agent | Focus |
| ----- | ----- |
| `csharp-mcp-expert` | MCP servers in C# |
| `go-mcp-expert` | MCP servers in Go |
| `java-mcp-expert` | MCP servers in Java |
| `kotlin-mcp-expert` | MCP servers in Kotlin |
| `php-mcp-expert` | MCP servers in PHP |
| `python-mcp-expert` | MCP servers in Python |
| `ruby-mcp-expert` | MCP servers in Ruby |
| `rust-mcp-expert` | MCP servers in Rust |
| `swift-mcp-expert` | MCP servers in Swift |
| `typescript-mcp-expert` | MCP servers in TypeScript |
| `mcp-m365-agent-expert` | MCP-based M365 Copilot agents |

### Salesforce Agents

| Agent | Focus |
| ----- | ----- |
| `salesforce-expert` | Salesforce platform guidance |
| `salesforce-apex-triggers` | Apex classes and triggers |
| `salesforce-aura-lwc` | LWC and Aura components |
| `salesforce-flow` | Salesforce Flow automation |
| `salesforce-visualforce` | Visualforce pages |

### Power BI & Power Platform Agents

| Agent | Focus |
| ----- | ----- |
| `power-bi-data-modeling-expert` | Star schema, relationships |
| `power-bi-dax-expert` | DAX formulas |
| `power-bi-performance-expert` | Power BI optimization |
| `power-bi-visualization-expert` | Report design, dashboards |
| `power-platform-expert` | Power Apps, Dataverse, connectors |
| `power-platform-mcp-integration-expert` | MCP custom connectors |

### Linux Specialist Agents

| Agent | Focus |
| ----- | ----- |
| `arch-linux-expert` | Arch Linux, pacman |
| `centos-linux-expert` | CentOS/RHEL, yum/dnf |
| `debian-linux-expert` | Debian, apt, policy |
| `fedora-linux-expert` | Fedora, dnf, SELinux |

### Testing & TDD Agents

| Agent | Focus |
| ----- | ----- |
| `tdd-red` | Write failing tests first |
| `tdd-green` | Make failing tests pass |
| `tdd-refactor` | Improve quality post-green |
| `playwright-tester` | Playwright E2E testing |
| `polyglot-test-generator` | Orchestrates test generation |
| `polyglot-test-researcher` | Test strategy research |
| `polyglot-test-planner` | Test plan creation |
| `polyglot-test-implementer` | Test implementation |
| `polyglot-test-builder` | Build & compile tests |
| `polyglot-test-tester` | Run test suites |
| `polyglot-test-fixer` | Fix compilation errors |
| `polyglot-test-linter` | Run linting/formatting |
| `qa-subagent` | QA sub-agent |
| `diffblue-cover` | Java unit tests via Diffblue |
| `stackhawk-security-onboarding` | StackHawk security testing setup |

### SE (Software Engineering) Team Agents

| Agent | Focus |
| ----- | ----- |
| `se-gitops-ci-specialist` | CI/CD, GitOps, deployment |
| `se-product-manager-advisor` | GitHub issues, product alignment |
| `se-responsible-ai-code` | Bias prevention, inclusive design |
| `se-security-reviewer` | OWASP Top 10, Zero Trust, LLM security |
| `se-system-architecture-reviewer` | Well-Architected review |
| `se-technical-writer` | Developer docs, tutorials |
| `se-ux-ui-designer` | JTBD analysis, user journey |

### Gem Team Agents

| Agent | Focus |
| ----- | ----- |
| `gem-orchestrator` | Gem team coordination |
| `gem-planner` | DAG-based planning |
| `gem-researcher` | Codebase context gathering |
| `gem-implementer` | TDD code changes |
| `gem-reviewer` | Security gatekeeper |
| `gem-devops` | Containers, CI/CD |
| `gem-documentation-writer` | Technical docs, diagrams |
| `gem-browser-tester` | E2E with Chrome/Playwright |

### Language & Framework Specialist Agents

| Agent | Focus |
| ----- | ----- |
| `CSharpExpert` | C# .NET development |
| `WinFormsExpert` | WinForms Designer apps |
| `expert-cpp-software-engineer` | Modern C++ |
| `expert-dotnet-software-engineer` | .NET design patterns |
| `expert-nextjs-developer` | Next.js App Router, RSC |
| `expert-react-frontend-engineer` | React 19, hooks, Server Components |
| `nuxt-expert` | Nuxt 3, Nitro, Vue 3 |
| `vuejs-expert` | Vue 3 Composition API |
| `laravel-expert-agent` | Laravel 12+ |
| `drupal-expert` | Drupal PHP 8.3+ |
| `pimcore-expert` | Pimcore CMS/DAM/PIM |
| `shopify-expert` | Shopify theme & app dev |
| `clojure-interactive-programming` | Clojure REPL-first |
| `winui3-expert` | WinUI 3, Windows App SDK |
| `dotnet-maui` | .NET MAUI cross-platform |
| `dotnet-self-learning-architect` | .NET 6+ senior architect |
| `dotnet-upgrade` | .NET modernization |
| `csharp-dotnet-janitor` | C#/.NET cleanup & tech debt |

### Database Agents

| Agent | Focus |
| ----- | ----- |
| `postgresql-dba` | PostgreSQL administration |
| `ms-sql-dba` | MS SQL Server via extension |
| `mongodb-performance-advisor` | MongoDB performance & indexes |
| `neo4j-docker-client-generator` | Neo4j Python client libraries |
| `neon-migration-specialist` | Zero-downtime Postgres migrations |
| `neon-optimization-analyzer` | Slow query identification |
| `oracle-to-postgres-migration-expert` | Oracle to PostgreSQL migration |

### Infrastructure & DevOps Agents

| Agent | Focus |
| ----- | ----- |
| `devops-expert` | DevOps infinity loop |
| `platform-sre-kubernetes` | SRE, K8s reliability |
| `github-actions-expert` | Secure CI/CD, OIDC, supply chain |
| `github-actions-node-upgrade` | Actions Node runtime upgrades |
| `droid` | Droid CLI, automation, CI/CD |

### Observability & Security Agents

| Agent | Focus |
| ----- | ----- |
| `agent-governance-reviewer` | AI governance, safety controls |
| `jfrog-sec` | JFrog security remediation |
| `dynatrace-expert` | Dynatrace observability |
| `elasticsearch-observability` | Elastic O11y, vector search |
| `defender-scout-kql` | Microsoft Defender KQL queries |
| `wg-code-sentinel` | Security-focused code review |
| `pagerduty-incident-responder` | PagerDuty incident resolution |

### Code Quality & Review Agents

| Agent | Focus |
| ----- | ----- |
| `code-reviewer` | Unbiased code review |
| `wg-code-alchemist` | Clean Code & SOLID design |
| `janitor` | Codebase cleanup |
| `tech-debt-remediation-plan` | Tech debt plans |
| `gilfoyle` | Sardonic code review |
| `critical-thinking` | Challenging assumptions |
| `doublecheck` | Three-layer verification pipeline |
| `refine-issue` | Issue/requirement refinement |

### Planning & Architecture Agents

| Agent | Focus |
| ----- | ----- |
| `context-architect` | Multi-file change planning |
| `implementation-plan` | Implementation plan generation |
| `plan` | Strategic planning & analysis |
| `planner` | Task planning mode |
| `hlbpa` | High-level architecture docs |
| `one-shot-feature-issue-planner` | Single-request feature plans |
| `modernization` | Legacy modernization planning |
| `principal-software-engineer` | Principal-level engineering |
| `software-engineer-agent-v1` | Expert software engineering |
| `adr-generator` | Architectural Decision Records |

### AI & Research Agents

| Agent | Focus |
| ----- | ----- |
| `research` | Deep web & file research |
| `research-technical-spike` | Technical spike validation |
| `context7` | Latest library docs & syntax |
| `comet-opik` | LLM tracing, Opik MCP |
| `scientific-paper-research` | Scientific paper retrieval |

### Content, Docs & Learning Agents

| Agent | Focus |
| ----- | ----- |
| `documentation-writer` | Technical documentation |
| `microsoft_learn_contributor` | Microsoft Learn docs |
| `taxcore-technical-writer` | TaxCore fiscal ecosystem docs |
| `technical-content-evaluator` | Training material evaluation |
| `prompt-builder` | Prompt engineering & validation |
| `prompt-engineer` | Prompt analysis & improvement |
| `prd` | Product Requirements Documents |
| `mentor` | Developer mentoring |
| `mentoring-juniors` | Socratic junior mentoring |
| `demonstrate-understanding` | Guided code understanding |
| `microsoft-study-mode` | Microsoft/Azure tutoring |

### Workflow & Orchestration Agents

| Agent | Focus |
| ----- | ----- |
| `rug-orchestrator` | Pure orchestration, delegates all work |
| `swe-subagent` | Implementation sub-agent |
| `qa-subagent` | QA sub-agent |
| `repo-architect` | Bootstraps agentic project structures |
| `meta-agentic-project-scaffold` | Multi-agent project scaffolding |
| `specification` | Specification document generation |
| `custom-agent-foundry` | Design & create VS Code agents |
| `task-planner` | Actionable task plans |
| `task-researcher` | Project analysis & research |

### Specialized Tool & Integration Agents

| Agent | Focus |
| ----- | ----- |
| `accessibility` | WCAG 2.1/2.2 compliance & a11y |
| `insiders-a11y-tracker` | VS Code Insiders a11y tracking |
| `lingodotdev-i18n` | i18n implementation |
| `markdown-accessibility-assistant` | Markdown accessibility |
| `aem-frontend-specialist` | AEM components, HTL, Tailwind |
| `electron-angular-native` | Electron/Angular/Node code review |
| `atlassian-requirements-to-jira` | Requirements to Jira epics |
| `amplitude-experiment-implementation` | Amplitude A/B experiments |
| `launchdarkly-flag-cleanup` | Feature flag cleanup |
| `monday-bug-fixer` | Monday.com context bug fixes |
| `reepl-linkedin` | LinkedIn content & scheduling |
| `code-tour` | VS Code CodeTour files |
| `address-comments` | Address GitHub PR review comments |
| `cast-imaging-impact-analysis` | CAST change impact analysis |
| `cast-imaging-software-discovery` | CAST architectural mapping |
| `cast-imaging-structural-quality-advisor` | CAST code quality |
| `apify-integration-expert` | Apify Actor integration |
| `python-notebook-sample-builder` | Azure/AI Jupyter notebooks |
| `octopus-deploy-release-notes-mcp` | Octopus Deploy release notes |
| `simple-app-idea-generator` | Brainstorm app ideas |
| `debug` | Systematic debugging mode |
| `devils-advocate` | Stress-test ideas |
| `email-classifier` | Gmail email classification |

---

## 🧩 Skills (~970)

Modular knowledge domains loaded on-demand. Organized into 40+ categories.

### 3D & WebGL

`3d-web-experience` · `threejs-skills` · `pan-3d-transition`

### ADK (Agent Development Kit)

`adk-cheatsheet` · `adk-deploy-guide` · `adk-dev-guide` · `adk-eval-guide` · `adk-observability-guide` · `adk-scaffold`

### AI & Machine Learning

`agent-evaluation` · `agent-goverance` · `agent-governance` · `agent-manager-skill` · `agent-memory-mcp` · `agent-memory-systems` · `agent-orchestration-improve-agent` · `agent-orchestration-multi-agent-optimize` · `agent-tool-builder` · `agentic-eval` · `ai-agents-architect` · `ai-engineer` · `ai-product` · `ai-prompt-engineering-safety-review` · `ai-wrapper-product` · `autonomous-agent-patterns` · `autonomous-agents` · `autoresearch` · `computer-vision-expert` · `context7-auto-research` · `crewai` · `embedding-strategies` · `eval-driven-dev` · `hybrid-search-implementation` · `imagen` · `langchain-architecture` · `langfuse` · `langgraph` · `langgraph-docs` · `llm-app-patterns` · `llm-application-dev-ai-assistant` · `llm-application-dev-langchain-agent` · `llm-application-dev-prompt-optimize` · `llm-evaluation` · `machine-learning-ops-ml-pipeline` · `microsoft-agent-framework` · `ml-engineer` · `ml-pipeline-workflow` · `mlops-engineer` · `model-recommendation` · `multi-agent-brainstorming` · `parallel-agents` · `prompt-caching` · `prompt-engineer` · `prompt-engineering` · `prompt-engineering-patterns` · `prompt-library` · `rag-engineer` · `rag-implementation` · `semantic-kernel` · `similarity-search-patterns` · `structured-autonomy-generate` · `structured-autonomy-implement` · `structured-autonomy-plan` · `vector-database-engineer` · `vector-index-tuning` · `voice-agents` · `voice-ai-development` · `voice-ai-engine-development` · `workflow-orchestration-patterns`

### Angular

`angular` · `angular-best-practices` · `angular-migration` · `angular-state-management` · `angular-ui-patterns`

### Architecture & Planning

`app-builder` · `architect-review` · `architecture` · `architecture-blueprint-generator` · `architecture-decision-records` · `architecture-patterns` · `backend-architect` · `brainstorming` · `breakdown-epic-arch` · `breakdown-epic-pm` · `breakdown-feature-implementation` · `breakdown-feature-prd` · `breakdown-plan` · `breakdown-test` · `c4-architecture-c4-architecture` · `c4-code` · `c4-component` · `c4-container` · `c4-context` · `cloud-architect` · `cloud-design-patterns` · `concise-planning` · `conductor-implement` · `conductor-manage` · `conductor-new-track` · `conductor-revert` · `conductor-setup` · `conductor-status` · `conductor-validator` · `context-driven-development` · `context-management-context-restore` · `context-management-context-save` · `context-manager` · `context-map` · `context-window-management` · `create-architectural-decision-record` · `create-implementation-plan` · `create-technical-spike` · `design-md` · `design-orchestration` · `deployment-pipeline-design` · `docs-architect` · `draw-io-diagram-generator` · `excalidraw-diagram-generator` · `folder-structure-blueprint-generator` · `hybrid-cloud-architect` · `hybrid-cloud-networking` · `mermaid-expert` · `monorepo-architect` · `monorepo-management` · `multi-cloud-architecture` · `plan-writing` · `plantuml-ascii` · `project-workflow-analysis-blueprint-generator` · `senior-architect` · `senior-fullstack` · `software-architecture` · `technology-stack-blueprint-generator` · `what-context-needed`

### Authentication & Security (App-Level)

`auth-implementation-patterns` · `broken-authentication` · `clerk-auth` · `gdpr-data-handling` · `nextjs-supabase-auth` · `pci-compliance` · `secrets-management` · `security-auditor` · `security-bluebook-builder` · `security-compliance-compliance-check` · `security-requirement-extraction` · `security-scanning-security-dependencies` · `security-scanning-security-hardening` · `security-scanning-security-sast`

### Azure & Cloud

`appinsights-instrumentation` · `aspire` · `az-cost-optimize` · `azure-architecture-autopilot` · `azure-deployment-preflight` · `azure-devops-cli` · `azure-functions` · `azure-pricing` · `azure-resource-health-diagnose` · `azure-resource-visualizer` · `azure-role-selector` · `azure-static-web-apps` · `cosmosdb-datamodeling` · `fabric-lakehouse`

### AWS

`aws-cdk-python-setup` · `aws-penetration-testing` · `aws-serverless` · `aws-skills`

### Backend Development

`api-design-principles` · `api-documentation-generator` · `api-documenter` · `api-patterns` · `api-security-best-practices` · `api-testing-observability-api-mock` · `async-python-patterns` · `backend-dev-guidelines` · `backend-development-feature-development` · `backend-security-coder` · `bullmq-specialist` · `bun-development` · `cc-skill-backend-patterns` · `cqrs-implementation` · `event-sourcing-architect` · `event-store-design` · `full-stack-orchestration-full-stack-feature` · `graphql` · `graphql-architect` · `inngest` · `intelligent-routing` · `microservices-patterns` · `nodejs-backend-patterns` · `nodejs-best-practices` · `openapi-spec-generation` · `openapi-to-application-code` · `saga-orchestration` · `trigger-dev` · `turborepo-caching` · `typespec-api-operations` · `typespec-create-agent` · `typespec-create-api-plugin` · `upstash-qstash`

### Blockchain & Web3

`blockchain-developer` · `defi-protocol-templates` · `nft-standards` · `solidity-security` · `web3-testing`

### Browser & Scraping

`browser-automation` · `chrome-devtools` · `exa-search` · `firecrawl-scraper` · `playwright-automation-fill-in-form` · `playwright-cli` · `playwright-explore-website` · `playwright-generate-test` · `playwright-skill` · `scrape-leads` · `shodan-reconnaissance` · `tavily-web`

### C# / .NET

`aspnet-minimal-api-openapi` · `csharp-async` · `csharp-docs` · `csharp-mcp-server-generator` · `csharp-mstest` · `csharp-nunit` · `csharp-pro` · `csharp-tunit` · `csharp-xunit` · `containerize-aspnet-framework` · `containerize-aspnetcore` · `dotnet-architect` · `dotnet-backend` · `dotnet-backend-patterns` · `dotnet-best-practices` · `dotnet-design-pattern-review` · `dotnet-timezone` · `dotnet-upgrade` · `ef-core` · `fluentui-blazor` · `nuget-manager`

### CI/CD & DevOps

`bazel-build-optimization` · `cicd-automation-workflow-automate` · `circleci-automation` · `create-github-action-workflow-specification` · `dependabot` · `deployment-engineer` · `deployment-procedures` · `deployment-validation-config-validate` · `devops-rollout-plan` · `devops-troubleshooter` · `gh-cli` · `git-advanced-workflows` · `git-commit` · `git-flow-branch-creator` · `git-pr-workflows-git-workflow` · `git-pr-workflows-onboard` · `git-pr-workflows-pr-enhance` · `git-pushing` · `github-actions-templates` · `github-automation` · `github-workflow-automation` · `gitlab-automation` · `gitlab-ci-patterns` · `gitops-workflow` · `helm-chart-scaffolding` · `k8s-manifest-generator` · `kubernetes-architect` · `modal-deploy` · `nx-workspace-patterns` · `on-call-handoff-patterns` · `platform-sre-kubernetes` · `publish-to-pages` · `render-automation` · `vercel-automation` · `vercel-deploy-claimable` · `vercel-deployment`

### Code Quality & Refactoring

`cc-skill-coding-standards` · `clean-code` · `code-documentation-code-explain` · `code-documentation-doc-generate` · `code-exemplars-blueprint-generator` · `code-refactoring-context-restore` · `code-refactoring-refactor-clean` · `code-refactoring-tech-debt` · `code-review` · `code-review-ai-ai-review` · `code-review-checklist` · `code-review-excellence` · `code-reviewer` · `codebase-cleanup-deps-audit` · `codebase-cleanup-refactor-clean` · `codebase-cleanup-tech-debt` · `codeql` · `codex-review` · `commit` · `conventional-commit` · `dependency-management-deps-audit` · `dependency-upgrade` · `editorconfig` · `find-bugs` · `fix-review` · `kaizen` · `legacy-modernizer` · `lint-and-validate` · `production-code-audit` · `quality-playbook` · `refactor` · `refactor-method-complexity-reduce` · `refactor-plan` · `review-and-refactor` · `ruff-recursive-fix` · `sast-configuration` · `shellcheck-configuration` · `write-coding-standards-from-file`

### Content & Document Generation

`audio-transcriber` · `beautiful-prose` · `comment-code-generate-a-tutorial` · `content-creator` · `content-marketer` · `copy-editing` · `copywriting` · `create-readme` · `daily-news-report` · `docx-official` · `documentation-generation-doc-generate` · `documentation-templates` · `documentation-writer` · `email-drafter` · `email-sequence` · `generate-report` · `markdown-to-html` · `meeting-minutes` · `mkdocs-translations` · `pdf-official` · `pdf-processing` · `pdf-service` · `pdftk-server` · `pptx-official` · `readme` · `readme-blueprint-generator` · `repo-story-time` · `social-content` · `tutorial-engineer` · `video-edit` · `x-article-publisher-skill` · `xlsx-official` · `youtube-summarizer`

### Copilot & GitHub Copilot

`copilot-cli-quickstart` · `copilot-instructions-blueprint-generator` · `copilot-sdk` · `copilot-spaces` · `copilot-usage-metrics` · `create-agentsmd` · `generate-custom-instructions-from-codebase` · `github-copilot-starter` · `microsoft-code-reference` · `microsoft-docs` · `suggest-awesome-github-copilot-agents` · `suggest-awesome-github-copilot-instructions` · `suggest-awesome-github-copilot-skills`

### Database

`bigquery-pipeline-audit` · `cc-skill-clickhouse-io` · `database-admin` · `database-architect` · `database-cloud-optimization-cost-optimize` · `database-design` · `database-migration` · `database-migrations-migration-observability` · `database-migrations-sql-migrations` · `database-optimizer` · `dbt-transformation-patterns` · `nosql-expert` · `neon-postgres` · `postgres-best-practices` · `postgresql` · `postgresql-code-review` · `postgresql-optimization` · `prisma-expert` · `projection-patterns` · `snowflake-semanticview` · `sql-code-review` · `sql-injection-testing` · `sql-optimization` · `sql-optimization-patterns` · `sql-pro` · `sqlmap-database-pentesting` · `using-neon`

### Data Engineering & Analytics

`airflow-dag-patterns` · `analyze-csv-files` · `data-analysis` · `data-engineer` · `data-engineering-data-driven-feature` · `data-engineering-data-pipeline` · `data-quality-frameworks` · `data-scientist` · `data-storytelling` · `datanalysis-credit-risk` · `last30days` · `market-sizing-analysis` · `risk-metrics-calculation` · `spark-optimization`

### Dataverse & Power Platform

`dataverse-python-advanced-patterns` · `dataverse-python-production-code` · `dataverse-python-quickstart` · `dataverse-python-usecase-builder` · `power-apps-code-app-scaffold` · `power-bi-dax-optimization` · `power-bi-model-design-review` · `power-bi-performance-troubleshooting` · `power-bi-report-design-consultation` · `power-platform-mcp-connector-suite` · `powerbi-modeling`

### Debugging & Diagnostics

`debugger` · `debugging-strategies` · `debugging-toolkit-smart-debug` · `distributed-debugging-debug-trace` · `distributed-tracing` · `error-debugging-error-analysis` · `error-debugging-error-trace` · `error-debugging-multi-agent-review` · `error-detective` · `error-diagnostics-error-analysis` · `error-diagnostics-error-trace` · `error-diagnostics-smart-debug` · `error-handling-patterns` · `find-bugs` · `systematic-debugging`

### Django / Python Web

`django-pro` · `fastapi-pro` · `fastapi-templates`

### Docker & Containers

`docker-expert` · `multi-stage-dockerfile`

### Documentation

`api-documenter` · `architecture-decision-records` · `code-documentation-code-explain` · `code-documentation-doc-generate` · `create-architectural-decision-record` · `documentation-generation-doc-generate` · `documentation-templates` · `documentation-writer` · `docs-architect` · `java-docs` · `oo-component-documentation` · `postmortem-writing` · `readme` · `readme-blueprint-generator`

### Elixir / Haskell / Scala / Other Languages

`elixir-pro` · `haskell-pro` · `julia-pro` · `scala-pro`

### Fintech & Payments

`backtesting-frameworks` · `billing-automation` · `plaid-fintech` · `payment-integration` · `paypal-integration` · `quant-analyst` · `risk-manager` · `startup-financial-modeling` · `stripe-automation` · `stripe-integration`

### Firebase / Supabase

`firebase` · `nextjs-supabase-auth` · `supabase-automation`

### Flutter / Mobile

`expo-deployment` · `flutter-expert` · `ios-developer` · `mobile-design` · `mobile-developer` · `mobile-security-coder` · `react-native-architecture` · `swiftui-expert-skill` · `upgrading-expo`

### Frontend & UI

`3d-web-experience` · `app-store-optimization` · `apple-appstore-reviewer` · `application-performance-performance-optimization` · `avalonia-layout-zafiro` · `avalonia-viewmodels-zafiro` · `avalonia-zafiro-development` · `browser-extension-builder` · `cc-skill-frontend-patterns` · `clerk-auth` · `core-components` · `design-website` · `dx-optimizer` · `figma-automation` · `form-cro` · `frontend-dev-guidelines` · `frontend-developer` · `frontend-mobile-development-component-scaffold` · `frontend-mobile-security-xss-scan` · `frontend-security-coder` · `frontend-slides` · `i18n-localization` · `interactive-portfolio` · `makepad-skills` · `markdown-to-html` · `onboarding-cro` · `page-cro` · `pan-3d-transition` · `paywall-upgrade-cro` · `penpot-uiux-design` · `popup-cro` · `premium-frontend-ui` · `radix-ui-design-system` · `react-best-practices` · `react-modernization` · `react-patterns` · `react-state-management` · `react-ui-patterns` · `remotion-best-practices` · `scroll-experience` · `signup-flow-cro` · `stitch-ui-design` · `superdesign` · `tailwind-design-system` · `tailwind-patterns` · `ui-skills` · `ui-ux-designer` · `ui-ux-pro-max` · `ui-visual-validator` · `vscode-ext-commands` · `vscode-ext-localization` · `wcag-audit-patterns` · `web-coder` · `web-design-guidelines` · `web-design-reviewer` · `web-performance-optimization`

### Game Development

`game-development` · `game-engine` · `godot-gdscript-patterns` · `unity-developer` · `unity-ecs-patterns` · `unreal-engine-cpp-pro`

### GCP & Cloud Run

`gcp-cloud-run`

### Go (Golang)

`go-concurrency-patterns` · `go-mcp-server-generator` · `go-playwright` · `golang-pro`

### GTM & Growth

`gtm-0-to-1-launch` · `gtm-ai-gtm` · `gtm-board-and-investor-communication` · `gtm-developer-ecosystem` · `gtm-enterprise-account-planning` · `gtm-enterprise-onboarding` · `gtm-operating-cadence` · `gtm-partnership-architecture` · `gtm-positioning-strategy` · `gtm-product-led-growth` · `gtm-technical-product-pricing` · `launch-strategy` · `micro-saas-launcher` · `pricing-strategy` · `startup-analyst` · `startup-business-analyst-business-case` · `startup-business-analyst-financial-projections` · `startup-business-analyst-market-opportunity` · `startup-metrics-framework`

### Java

`create-spring-boot-java-project` · `java-add-graalvm-native-image-support` · `java-docs` · `java-junit` · `java-mcp-server-generator` · `java-pro` · `java-refactoring-extract-method` · `java-refactoring-remove-parameter` · `java-springboot` · `spring-boot-testing`

### JavaScript / TypeScript

`javascript-mastery` · `javascript-pro` · `javascript-testing-patterns` · `javascript-typescript-jest` · `javascript-typescript-typescript-scaffold` · `modern-javascript-patterns` · `typescript-advanced-types` · `typescript-expert` · `typescript-mcp-server-generator` · `typescript-pro`

### Kotlin

`create-spring-boot-kotlin-project` · `kotlin-mcp-server-generator` · `kotlin-springboot`

### Linux & Shell

`arch-linux-triage` · `bash-defensive-patterns` · `bash-linux` · `bash-pro` · `bats-testing-patterns` · `busybox-on-windows` · `centos-linux-triage` · `debian-linux-triage` · `fedora-linux-triage` · `linux-privilege-escalation` · `linux-shell-scripting` · `posix-shell-pro` · `powershell-windows` · `windows-privilege-escalation`

### MCP (Model Context Protocol)

`mcp-cli` · `mcp-copilot-studio-server-generator` · `mcp-create-adaptive-cards` · `mcp-create-declarative-agent` · `mcp-deploy-manage-agents` · `php-mcp-server-generator` · `python-mcp-server-generator` · `ruby-mcp-server-generator` · `rust-mcp-server-generator` · `swift-mcp-server-generator`

### Minecraft / Game Server

`minecraft-bukkit-pro`

### Monitoring & Observability

`distributed-tracing` · `grafana-dashboards` · `istio-traffic-management` · `loki-mode` · `observability-engineer` · `observability-monitoring-monitor-setup` · `observability-monitoring-slo-implement` · `prometheus-configuration` · `service-mesh-expert` · `service-mesh-observability` · `slo-implementation`

### Next.js

`next-intl-add-language` · `nextjs-app-router-patterns` · `nextjs-best-practices` · `nextjs-supabase-auth`

### No-Code / Workflow Automation

`automate-this` · `automate-whatsapp` · `make-automation` · `n8n-code-python` · `n8n-mcp-tools-expert` · `n8n-node-configuration` · `workflow-automation` · `zapier-make-patterns`

### PHP

`php-mcp-server-generator` · `php-pro`

### Product Management

`competitive-landscape` · `competitor-alternatives` · `create-github-issue-feature-from-specification` · `create-github-issues-feature-from-implementation-plan` · `create-github-issues-for-unmet-specification-requirements` · `create-github-pull-request-from-specification` · `create-proposal` · `create-specification` · `gen-specs-as-issues` · `github-issues` · `my-issues` · `my-pull-requests` · `prd` · `product-manager-toolkit` · `update-specification`

### Python

`async-python-patterns` · `python-development-python-scaffold` · `python-packaging` · `python-patterns` · `python-performance-optimization` · `python-pro` · `python-testing-patterns` · `uv-package-manager`

### React

`react-best-practices` · `react-modernization` · `react-native-architecture` · `react-patterns` · `react-state-management` · `react-ui-patterns` · `unit-test-vue-pinia`

### Ruby

`ruby-mcp-server-generator` · `ruby-pro` · `skill-rails-upgrade`

### Rust

`memory-safety-patterns` · `rust-async-patterns` · `rust-mcp-server-generator` · `rust-pro` · `systems-programming-rust-project`

### Salesforce

`salesforce-automation` · `salesforce-development`

### SaaS Automation (via Composio/Rube MCP)

`activecampaign-automation` · `airtable-automation` · `amplitude-automation` · `asana-automation` · `bamboohr-automation` · `basecamp-automation` · `box-automation` · `brevo-automation` · `cal-com-automation` · `calendly-automation` · `canva-automation` · `changelog-automation` · `clickup-automation` · `close-automation` · `coda-automation` · `confluence-automation` · `convertkit-automation` · `datadog-automation` · `discord-automation` · `docusign-automation` · `dropbox-automation` · `figma-automation` · `freshdesk-automation` · `freshservice-automation` · `github-automation` · `gitlab-automation` · `gmail-automation` · `gmail-inbox` · `gmail-label` · `google-analytics-automation` · `google-calendar-automation` · `google-drive-automation` · `googlesheets-automation` · `helpdesk-automation` · `hubspot-automation` · `instagram-automation` · `instantly-autoreply` · `instantly-campaigns` · `intercom-automation` · `jira-automation` · `klaviyo-automation` · `linear-automation` · `linkedin-automation` · `mailchimp-automation` · `microsoft-teams-automation` · `miro-automation` · `mixpanel-automation` · `monday-automation` · `notion-automation` · `one-drive-automation` · `outlook-automation` · `outlook-calendar-automation` · `pagerduty-automation` · `pipedrive-automation` · `posthog-automation` · `postmark-automation` · `reddit-automation` · `salesforce-automation` · `segment-automation` · `segment-cdp` · `sendgrid-automation` · `sentry-automation` · `shopify-automation` · `slack-automation` · `square-automation` · `stripe-automation` · `telegram-automation` · `tiktok-automation` · `todoist-automation` · `trello-automation` · `twitter-automation` · `vercel-automation` · `webflow-automation` · `wrike-automation` · `youtube-automation` · `zendesk-automation` · `zoho-crm-automation` · `zoom-automation`

### Security & Penetration Testing

`active-directory-attacks` · `anti-reversing-techniques` · `api-fuzzing-bug-bounty` · `api-security-best-practices` · `attack-tree-construction` · `aws-penetration-testing` · `binary-analysis-patterns` · `burp-suite-testing` · `cloud-penetration-testing` · `ethical-hacking-methodology` · `ffuf-claude-skill` · `file-path-traversal` · `file-uploads` · `firmware-analyst` · `html-injection-testing` · `idor-testing` · `linux-privilege-escalation` · `malware-analyst` · `memory-forensics` · `metasploit-framework` · `mtls-configuration` · `pentest-checklist` · `pentest-commands` · `privilege-escalation-methods` · `protocol-reverse-engineering` · `red-team-tactics` · `red-team-tools` · `reverse-engineer` · `scanning-tools` · `secret-scanning` · `smtp-penetration-testing` · `sql-injection-testing` · `sqlmap-database-pentesting` · `ssh-penetration-testing` · `stride-analysis-patterns` · `threat-mitigation-mapping` · `threat-modeling-expert` · `top-web-vulnerabilities` · `vulnerability-scanner` · `web3-testing` · `windows-privilege-escalation` · `wireshark-analysis` · `wordpress-penetration-testing` · `xss-html-injection`

### SEO & Growth Marketing

`app-store-optimization` · `geo-fundamentals` · `programmatic-seo` · `schema-markup` · `seo-audit` · `seo-authority-builder` · `seo-cannibalization-detector` · `seo-content-auditor` · `seo-content-planner` · `seo-content-refresher` · `seo-content-writer` · `seo-fundamentals` · `seo-keyword-strategist` · `seo-meta-optimizer` · `seo-snippet-hunter` · `seo-structure-architect`

### Shopify & E-Commerce

`shopify-apps` · `shopify-automation` · `shopify-development`

### Swift / iOS / macOS

`ios-developer` · `swift-mcp-server-generator` · `swiftui-expert-skill`

### Telegram & Communication Bots

`discord-bot-architect` · `slack-bot-builder` · `telegram-bot-builder` · `telegram-mini-app` · `twilio-communications`

### Testing & QA

`bats-testing-patterns` · `e2e-testing-patterns` · `javascript-testing-patterns` · `javascript-typescript-jest` · `performance-testing-review-ai-review` · `performance-testing-review-multi-agent-review` · `playwright-skill` · `pytest-coverage` · `python-testing-patterns` · `scoutqa-test` · `tdd-orchestrator` · `tdd-workflow` · `tdd-workflows-tdd-cycle` · `tdd-workflows-tdd-green` · `tdd-workflows-tdd-red` · `tdd-workflows-tdd-refactor` · `test-automator` · `test-fixing` · `testing-patterns` · `unit-test-vue-pinia` · `unit-testing-test-generate` · `webapp-testing`

### Vue.js / Nuxt

`nuxt-expert` (agent) · `unit-test-vue-pinia`

### Whatsapp & Messaging

`automate-whatsapp` · `observe-whatsapp`

### Miscellaneous / Utility

`add-educational-comments` · `add-webhook` · `address-github-comments` · `algolia-search` · `analytics-tracking` · `arm-cortex-expert` · `automate-this` · `behavioral-modes` · `blockrun` · `boost-prompt` · `brand-guidelines-anthropic` · `brand-guidelines-community` · `business-analyst` · `cc-skill-continuous-learning` · `cc-skill-project-guidelines-example` · `cc-skill-security-review` · `cc-skill-strategic-compact` · `classify-leads` · `claude-ally-health` · `claude-code-guide` · `claude-d3js-skill` · `claude-scientific-skills` · `claude-speed-reader` · `claude-win11-speckit-update-skill` · `cli-mastery` · `culture-index` · `customer-support` · `daily-prep` · `declarative-agents` · `deep-research` · `design-orchestration` · `discord-bot-architect` · `email-systems` · `employment-contract-templates` · `environment-setup-guide` · `file-organizer` · `find-skills` · `first-ask` · `free-tool-strategy` · `geofeed-tuner` · `gmaps-leads` · `hr-pro` · `hubspot-integration` · `hugging-face-cli` · `hugging-face-jobs` · `image-manipulation-image-magick` · `incident-responder` · `incident-response-incident-response` · `incident-response-smart-fix` · `incident-runbook-templates` · `infinite-gratitude` · `internal-comms-anthropic` · `internal-comms-community` · `issue-fields-migration` · `iterate-pr` · `kaizen` · `kpi-dashboard-design` · `legal-advisor` · `linkerd-patterns` · `literature-research` · `make-repo-contribution` · `make-skill-template` · `marketing-ideas` · `marketing-psychology` · `memory-merger` · `mentoring-juniors` · `microsoft-skill-creator` · `mobile-security-coder` · `moodle-external-api-development` · `msstore-cli` · `my-pull-requests` · `my-issues` · `nanobanana-ppt-skills` · `napkin` · `network-101` · `network-engineer` · `noob-mode` · `notion-template-business` · `observability-engineer` · `oss-hunter` · `paid-ads` · `payment-integration` · `personal-tool-builder` · `plaid-fintech` · `postmortem-writing` · `profile-cro` · `protocol-reverse-engineering` · `quasi-coder` · `recreate-thumbnails` · `referral-program` · `remember` · `remember-interactive-programming` · `research-engineer` · `risk-manager` · `roll-dice` · `roundup` · `roundup-setup` · `sales-automator` · `screen-reader-testing` · `screenshots` · `search-specialist` · `sharp-edges` · `shuffle-json-data` · `skill-developer` · `skill-seekers` · `skool-monitor` · `skool-rag` · `sponsor-finder` · `team-collaboration-issue` · `team-collaboration-standup-notes` · `team-composition-analysis` · `title-variants` · `tldr-prompt` · `track-management` · `transloadit-media-processing` · `upwork-apply` · `varlock-claude-skill` · `vexor` · `viral-generator-builder` · `web-performance-optimization` · `welcome-email` · `winapp-cli` · `winmd-api-search` · `winui3-migration-guide` · `workiq-copilot` · `youtube-outliers` · `cross-niche-outliers` · `casualize-names` · `convert-plaintext-to-md` · `conversation-memory` · `create-llms` · `create-pr` · `create-tldr-page` · `fal-audio` · `fal-generate` · `fal-image-edit` · `fal-platform` · `fal-upscale` · `fal-workflow` · `finnish-humanizer` · `fp-ts-errors` · `fp-ts-pragmatic` · `fp-ts-react` · `framework-migration-code-migrate` · `framework-migration-deps-upgrade` · `framework-migration-legacy-modernize` · `legacy-circuit-mockups` · `linear-claude-skill` · `loki-mode` · `nano-banana-pro-openrouter` · `network-101` · `noob-mode` · `oo-component-documentation` · `sandbox-npm-install` · `skill-rails-upgrade` · `social-content` · `superpowers-lab` · `update-avm-modules-in-bicep` · `update-implementation-plan` · `update-llms` · `update-markdown-file-index` · `web3-testing`

---

## 🔄 Global Workflows (20)

Slash command procedures. Invoke with `/command`.

| Command | File | Description |
| ------- | ---- | ----------- |
| `/brainstorm` | `brainstorm.md` | Socratic discovery, 3+ options with tradeoffs |
| `/commit` | `commit.md` | Conventional commit message generation |
| `/conductor` | `conductor.md` | Project context management (setup, scan, validate) |
| `/create` | `create.md` | Create new applications via agent orchestration |
| `/create-tutorials` | `create-tutorials.md` | Tutorial creation workflow |
| `/create_workstreams` | `create_workstreams.md` | Multi-stream workload creation |
| `/debug` | `debug.md` | Systematic problem investigation |
| `/deploy` | `deploy.md` | Production deployment with pre-flight checks |
| `/double-check` | `double-check.md` | Three-layer output verification |
| `/enhance` | `enhance.md` | Iterative feature additions to existing apps |
| `/fal` | `fal.md` | Route fal.ai requests (generate, upscale, edit, audio) |
| `/nextjs` | `nextjs.md` | Build or enhance Next.js App Router applications |
| `/orchestrate` | `orchestrate.md` | Multi-agent coordination (min 3 agents) |
| `/plan` | `plan.md` | Project planning with dynamic naming |
| `/preview` | `preview.md` | Preview server start/stop/status |
| `/react-spa` | `react-spa.md` | Build or enhance React SPA applications |
| `/status` | `status.md` | Display agent and project status board |
| `/superdesign` | `superdesign.md` | UI/UX design workflow via superdesign CLI |
| `/test` | `test.md` | Test generation, execution, and coverage |
| `/ui-ux-pro-max` | `ui-ux-pro-max.md` | Design with 50+ styles, 97 palettes, 57 fonts |

---

## 🔌 Plugins (53)

Bundled multi-agent/skill packs organized by domain.

| Plugin | Purpose |
| ------ | ------- |
| `automate-this` | Generic automation workflows |
| `awesome-copilot` | GitHub Copilot curated agents & skills |
| `azure-cloud-development` | Azure cloud development packs |
| `cast-imaging` | CAST Imaging software analysis |
| `clojure-interactive-programming` | Clojure REPL-first development |
| `context-engineering` | Context management & engineering |
| `copilot-sdk` | GitHub Copilot SDK integration |
| `csharp-dotnet-development` | C#/.NET full development suite |
| `csharp-mcp-development` | C# MCP server development |
| `database-data-management` | Database & data management bundle |
| `dataverse-sdk-for-python` | Dataverse Python SDK |
| `devops-oncall` | DevOps on-call runbooks |
| `doublecheck` | Output verification workflows |
| `edge-ai-tasks` | Edge AI task automation |
| `fastah-ip-geo-tools` | IP geolocation tools |
| `flowstudio-power-automate` | Power Automate via FlowStudio |
| `frontend-web-dev` | Frontend web development bundle |
| `gem-team` | Full Gem team agent pack |
| `go-mcp-development` | Go MCP server development |
| `java-development` | Java development suite |
| `java-mcp-development` | Java MCP server development |
| `kotlin-mcp-development` | Kotlin MCP server development |
| `mcp-m365-copilot` | MCP for M365 Copilot agents |
| `napkin` | Napkin diagramming integration |
| `noob-mode` | Beginner-friendly mode |
| `openapi-to-application-csharp-dotnet` | OpenAPI → C#/.NET app |
| `openapi-to-application-go` | OpenAPI → Go app |
| `openapi-to-application-java-spring-boot` | OpenAPI → Java Spring Boot app |
| `openapi-to-application-nodejs-nestjs` | OpenAPI → Node.js NestJS app |
| `openapi-to-application-python-fastapi` | OpenAPI → Python FastAPI app |
| `oracle-to-postgres-migration-expert` | Oracle to PostgreSQL migration pack |
| `ospo-sponsorship` | Open source sponsorship management |
| `partners` | Partner integration pack |
| `pcf-development` | PCF (Pivotal Cloud Foundry) development |
| `php-mcp-development` | PHP MCP server development |
| `polyglot-test-agent` | Full polyglot testing agent suite |
| `power-apps-code-apps` | Power Apps code apps |
| `power-bi-development` | Power BI development suite |
| `power-platform-mcp-connector-development` | Power Platform MCP connectors |
| `project-planning` | Full project planning workflow |
| `python-mcp-development` | Python MCP server development |
| `roundup` | Content roundup workflows |
| `ruby-mcp-development` | Ruby MCP server development |
| `rug-agentic-workflow` | RUG pure orchestration workflow |
| `rust-mcp-development` | Rust MCP server development |
| `security-best-practices` | Security best practices pack |
| `software-engineering-team` | Full SE team agent bundle |
| `structured-autonomy` | Structured autonomy workflows |
| `swift-mcp-development` | Swift MCP server development |
| `technical-spike` | Technical spike research pack |
| `testing-automation` | Testing automation suite |
| `typescript-mcp-development` | TypeScript MCP server development |
| `typespec-m365-copilot` | TypeSpec for M365 Copilot |
| `winui3-development` | WinUI 3 development pack |

---

## 📜 Rules (1)

Global behavior rules that apply across all agents and skills.

| File | Priority | Description |
| ---- | -------- | ----------- |
| `GEMINI.md` | P0 (highest) | Single source of truth for AI behavior. Controls: skill loading protocol, request classification (QUESTION/SIMPLE CODE/COMPLEX CODE/DESIGN/SLASH CMD), intelligent agent routing, output format standards, git discipline, and quality gates. Overrides all agent and skill instructions. |

### GEMINI.md Key Controls

| Section | Behavior |
| ------- | -------- |
| **Request Classifier** | Routes QUESTION → TIER 0, SIMPLE CODE → TIER 0+1, COMPLEX CODE → TIER 0+1+Agent |
| **Agent Routing** | Auto-detects domains, selects best specialist, informs user |
| **Skill Loading** | Reads SKILL.md index first → loads only matching sections |
| **Output Format** | Enforces structured responses, file diffs, commit discipline |
| **Quality Gates** | Security, lint, tests, SEO checks before delivery |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
                                            ↓
                                    Read references/
                                            ↓
                                    Read scripts/
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

---

## 📊 Statistics

| Metric | Value |
| ------ | ----- |
| **Total Agents** | ~200 (209 files) |
| **Total Skills** | ~970 (973 directories) |
| **Total Global Workflows** | 20 |
| **Total Plugins** | 53 |
| **Total Rules** | 1 (GEMINI.md) |
| **Agent Categories** | 20+ groupings |
| **Skill Categories** | 40+ groupings |
| **Coverage** | Full-stack dev, DevOps, Security, AI/ML, MCP, SaaS automation, Azure/Cloud, Salesforce, Power Platform, Linux, Content generation, Game Dev, Mobile, SEO, Blockchain |

*Last updated: 2026-05-07*

---

## 🔗 Quick Reference

| Need | Agent | Skills |
| ---- | ----- | ------ |
| Web App | `frontend-specialist` | `react-patterns`, `nextjs-best-practices` |
| API | `backend-specialist` | `api-patterns`, `nodejs-best-practices` |
| Mobile | `mobile-developer` | `mobile-design`, `flutter-expert` |
| Database | `database-architect` | `database-design`, `prisma-expert` |
| Security Audit | `security-auditor` | `vulnerability-scanner`, `xss-html-injection` |
| Pentesting | `penetration-tester` | `red-team-tactics`, `metasploit-framework` |
| Testing | `test-engineer` | `testing-patterns`, `webapp-testing` |
| TDD | `tdd-red` + `tdd-green` + `tdd-refactor` | `tdd-workflow` |
| Debug | `debugger` | `systematic-debugging` |
| Plan | `project-planner` | `brainstorming`, `plan-writing` |
| SaaS Ops | `orchestrator` | `wrike-automation`, `zendesk-automation` |
| Content | `documentation-writer` | `xlsx-official`, `youtube-summarizer` |
| AI/ML | `backend-specialist` | `rag-engineer`, `langchain-architecture` |
| Azure IaC | `azure-iac-generator` | `azure-functions`, `az-cost-optimize` |
| MCP Server | `python-mcp-expert` / `typescript-mcp-expert` | `python-mcp-server-generator` |
| Salesforce | `salesforce-expert` | `salesforce-automation` |
| Power BI | `power-bi-dax-expert` | `power-bi-dax-optimization` |
| Oracle→PG | `oracle-to-postgres-migration-expert` | `creating-oracle-to-postgres-master-migration-plan` |
| Multi-Agent | `rug-orchestrator` | `parallel-agents`, `workflow-orchestration-patterns` |
| Beast Mode | `4.1-Beast` / `gpt-5-beast-mode` | All skills auto-loaded |
