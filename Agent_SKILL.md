# 🧠 GitHub Copilot Customization Repo — Complete Understanding Guide

> A deep-dive reference for every component in this repo: what it is, how to create it, how to run/use it, and real examples.

---

## Table of Contents

1. [Repository Structure & `.github` Folder](#1-repository-structure--github-folder)
2. [🤖 Agents](#2--agents)
3. [📋 Instructions](#3--instructions)
4. [🎯 Skills](#4--skills)
5. [🔌 Plugins](#5--plugins)
6. [🪝 Hooks](#6--hooks)
7. [⚡ Agentic Workflows](#7--agentic-workflows)
8. [🍳 Cookbook](#8--cookbook)
9. [How All Components Work Together](#9-how-all-components-work-together)

---

## 1. Repository Structure & `.github` Folder

### What is the `.github` folder?

The `.github` folder is a **special directory** recognized by GitHub. It holds configuration that controls GitHub features — Actions, Copilot customizations, issue templates, PR templates, and more.

```
.github/
├── copilot/                    # Copilot-specific customizations
│   ├── agents/                 # Custom Copilot agents
│   ├── instructions/           # Auto-applied coding standards
│   ├── skills/                 # Bundled skill folders
│   └── plugins/                # Plugin bundles
├── workflows/                  # GitHub Actions (standard + agentic)
├── hooks/                      # Copilot session hooks
├── PULL_REQUEST_TEMPLATE.md
├── ISSUE_TEMPLATE/
└── copilot-instructions.md     # Global Copilot instructions file
```

### The special `copilot-instructions.md`

This file lives at `.github/copilot-instructions.md` and provides **workspace-wide context** to GitHub Copilot. Every Copilot chat session in this repo automatically includes it.

**How to create it:**

```markdown
<!-- .github/copilot-instructions.md -->

# Project Context

This is a TypeScript monorepo using pnpm workspaces.

## Coding Standards
- Use `const` over `let` wherever possible
- Prefer named exports over default exports
- All async functions must handle errors with try/catch

## Architecture
- Services live in `packages/services/`
- Shared utilities live in `packages/utils/`
- Never import across package boundaries without going through the public API
```

**How Copilot uses it:** Every time you open Copilot Chat in VS Code or GitHub.com for this repo, these instructions are silently injected into the context — no `@` mention needed.

---

## 2. 🤖 Agents

### What is a Copilot Agent?

An **agent** is a specialized Copilot persona with a custom name, description, system prompt, and a set of connected tools (MCP servers). Instead of talking to generic Copilot, you invoke `@my-agent` and get a focused expert.

### Folder Structure

```
.github/copilot/agents/
└── my-agent/
    ├── agent.yml         # Agent metadata and configuration
    └── system-prompt.md  # The agent's personality and instructions
```

### How to Create an Agent

**Step 1 — Create `agent.yml`:**

```yaml
# .github/copilot/agents/db-expert/agent.yml

name: db-expert
display_name: "Database Expert"
description: "Specialist in PostgreSQL query optimization, schema design, and migrations"
version: "1.0.0"

# MCP servers this agent has access to
mcp_servers:
  - name: postgres-mcp
    url: https://mcp.example.com/postgres
    description: "Live database introspection and query execution"

# Which skills this agent can use
skills:
  - sql-formatter
  - migration-generator

# Restrict what the agent can read/touch
permissions:
  read:
    - "db/**"
    - "migrations/**"
  write:
    - "migrations/**"
```

**Step 2 — Create `system-prompt.md`:**

```markdown
# Database Expert Agent

You are a senior PostgreSQL database engineer with 15 years of experience.

## Your Responsibilities
- Analyze slow queries and suggest optimized versions with EXPLAIN output
- Design normalized schemas following 3NF unless denormalization is justified
- Write Flyway/Liquibase-compatible migration scripts

## Rules
- Always wrap destructive operations in transactions
- Never suggest dropping columns without a deprecation migration first
- Prefer CTEs over subqueries for readability

## Output Format
When suggesting a query change, always show:
1. The original query
2. The optimized query
3. The expected improvement and why
```

### How to Use an Agent

In **GitHub Copilot Chat** (VS Code or GitHub.com):

```
@db-expert Why is this query scanning 2M rows when there are only 50k users?

SELECT u.*, o.* FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'pending';
```

In **GitHub.com PR Review:**

```
@db-expert Please review the schema changes in this migration file
```

---

## 3. 📋 Instructions

### What are Instructions?

**Instructions** are coding standards and rules that Copilot applies **automatically based on file patterns**. They are like `.editorconfig` but for AI behavior — no need to paste context into every chat.

### Folder Structure

```
.github/copilot/instructions/
├── typescript.instructions.md     # Applied to *.ts, *.tsx files
├── python.instructions.md         # Applied to *.py files
├── testing.instructions.md        # Applied to *.test.*, *.spec.* files
├── api.instructions.md            # Applied to src/api/**
└── react.instructions.md          # Applied to src/components/**
```

### How to Create Instructions

Each file has a **YAML front-matter** declaring which files it applies to, followed by the actual instructions in Markdown.

**Example — TypeScript instructions:**

```markdown
---
applyTo:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript Coding Standards

## Types
- Prefer `interface` over `type` for object shapes that may be extended
- Never use `any`; use `unknown` and narrow with type guards
- Always type function return values explicitly

## Imports
- Use path aliases (`@/components/...`) never relative `../../` paths
- Group imports: external → internal → types (separated by blank lines)

## Error Handling
- Use `Result<T, E>` pattern from our `utils/result.ts` for operations that can fail
- Never swallow errors with empty `catch {}` blocks
```

**Example — Testing instructions:**

```markdown
---
applyTo:
  - "**/*.test.ts"
  - "**/*.spec.ts"
  - "**/*.test.tsx"
---

# Testing Standards

## Structure
- Use `describe` blocks that mirror the module being tested
- Each `it()` or `test()` description should complete the sentence "it should..."
- AAA pattern: Arrange → Act → Assert with blank lines between sections

## Mocking
- Use `vi.mock()` at the module level, never inside test functions
- Always restore mocks with `afterEach(() => vi.restoreAllMocks())`

## Assertions
- Prefer `toEqual` over `toBe` for objects
- Use `toMatchInlineSnapshot()` for complex output — never hardcoded strings
```

### How Instructions Are Applied

Instructions activate **automatically** when you:
- Open a file matching the `applyTo` pattern and use Copilot inline suggestions
- Ask Copilot Chat while a matching file is in context
- Run a Copilot-powered code review on a PR containing matching files

No manual invocation needed — Copilot reads the applicable instructions silently.

---

## 4. 🎯 Skills

### What is a Skill?

A **skill** is a self-contained folder that teaches Copilot (or an agent) how to perform a specific task. It bundles:
- A `SKILL.md` with step-by-step instructions for the AI
- Supporting assets (scripts, templates, reference files)
- A `.skill` package manifest for distribution

Think of skills as **reusable AI procedures** — like npm packages, but for AI behavior.

### Folder Structure

```
.github/copilot/skills/
└── generate-api-client/
    ├── SKILL.md              # The AI's instruction manual for this skill
    ├── templates/
    │   ├── client.ts.hbs     # Handlebars template for the client
    │   └── types.ts.hbs
    ├── scripts/
    │   └── validate-spec.py  # Helper script the AI can run
    └── generate-api-client.skill  # Package manifest
```

### How to Create a Skill

**`SKILL.md` — The core of every skill:**

```markdown
# Skill: Generate API Client

## Purpose
Generate a fully-typed TypeScript API client from an OpenAPI 3.x spec file.

## When to Use This Skill
Trigger this skill when the user asks to:
- "Generate a client for this API"
- "Create TypeScript types from this OpenAPI spec"
- "Build an API SDK"

## Prerequisites
Check that these exist before starting:
1. An OpenAPI spec file (`.yaml` or `.json`) is present in the repo
2. The `templates/` folder is available at the skill path

## Step-by-Step Instructions

### Step 1 — Parse the spec
Run the validation script first:
```bash
python scripts/validate-spec.py path/to/openapi.yaml
```
If it exits with errors, report them to the user and stop.

### Step 2 — Generate types
For each schema in `components/schemas`, create a TypeScript interface using the `types.ts.hbs` template.

### Step 3 — Generate methods
For each path + method combination, create a typed async function using `client.ts.hbs`.

### Step 4 — Output
Write files to `src/api/generated/`. Warn the user these files are auto-generated and should not be edited manually.

## Output Format
Always produce:
- `src/api/generated/types.ts`
- `src/api/generated/client.ts`
- A summary of what was generated
```

**`.skill` manifest:**

```yaml
# generate-api-client.skill
name: generate-api-client
version: "1.2.0"
description: "Generates a typed TypeScript API client from OpenAPI specs"
author: "your-org"
main: SKILL.md
assets:
  - templates/
  - scripts/
```

### How to Use a Skill

**Via an agent that has the skill registered:**

```
@api-agent Generate a TypeScript client from the spec at docs/openapi.yaml
```

**By referencing the skill directly in chat (if skill discovery is enabled):**

```
Use the generate-api-client skill on ./api/spec.json
```

**Running a skill's script manually (for debugging):**

```bash
python .github/copilot/skills/generate-api-client/scripts/validate-spec.py api/spec.json
```

---

## 5. 🔌 Plugins

### What is a Plugin?

A **plugin** is a **curated bundle** of agents and skills packaged together for a specific workflow or persona. Where a skill is a single procedure and an agent is a single persona, a plugin is the complete toolkit for a domain (e.g., "full-stack development", "DevOps", "data engineering").

### Folder Structure

```
.github/copilot/plugins/
└── fullstack-dev/
    ├── plugin.yml            # What's included and how it's activated
    ├── agents/
    │   ├── frontend-agent/   # A specialized agent bundled with this plugin
    │   └── backend-agent/
    └── skills/
        ├── component-generator/
        └── api-scaffolder/
```

### How to Create a Plugin

**`plugin.yml`:**

```yaml
# .github/copilot/plugins/fullstack-dev/plugin.yml

name: fullstack-dev
display_name: "Full-Stack Development Suite"
version: "2.0.0"
description: >
  Complete toolkit for full-stack TypeScript development.
  Includes agents for frontend (React) and backend (Node/Express)
  work, plus skills for scaffolding components and APIs.

# Agents included in this plugin
agents:
  - path: agents/frontend-agent
    name: frontend
  - path: agents/backend-agent
    name: backend

# Skills available to all agents in this plugin
skills:
  - path: skills/component-generator
  - path: skills/api-scaffolder
  - name: generate-api-client          # Reference a skill from the global registry
    version: "^1.2.0"

# MCP servers available to all agents in this plugin
mcp_servers:
  - name: github-mcp
    url: https://mcp.github.com/sse
  - name: figma-mcp
    url: https://mcp.figma.com/sse

# Shared instructions injected into every agent in this plugin
shared_instructions: |
  This is a TypeScript monorepo. Always use the workspace root tsconfig.
  Never mix CommonJS and ESM in the same package.
```

### How to Use a Plugin

Plugins are activated per-repository or per-team in your GitHub organization settings.

**Activate in repo settings:**

```
GitHub Repo Settings → Copilot → Plugins → Enable "fullstack-dev"
```

**Then use the bundled agents:**

```
@frontend Create a new React component for the user profile card based on the Figma design
@backend Scaffold a REST endpoint for PATCH /users/:id with validation
```

---

## 6. 🪝 Hooks

### What is a Hook?

**Hooks** are automated actions that Copilot triggers at specific points in an agent session — before a response, after a tool call, when a file is written, etc. They act as **middleware** for AI sessions.

Use hooks to:
- Auto-run linters after Copilot edits a file
- Post a Slack notification when Copilot opens a PR
- Validate generated code before it's shown to the user
- Log AI actions for audit trails

### Folder Structure

```
.github/hooks/
├── pre-edit.yml          # Fires before Copilot edits a file
├── post-edit.yml         # Fires after Copilot writes a file
├── pre-tool-call.yml     # Fires before any MCP tool is called
├── post-pr-open.yml      # Fires after Copilot opens a PR
└── session-end.yml       # Fires when the Copilot session ends
```

### Hook Lifecycle Events

| Event | When it fires |
|---|---|
| `session.start` | Copilot agent session begins |
| `session.end` | Agent session completes or is abandoned |
| `file.before_write` | Before Copilot writes/edits a file |
| `file.after_write` | After a file is written successfully |
| `tool.before_call` | Before any MCP tool is invoked |
| `tool.after_call` | After an MCP tool returns a result |
| `pr.opened` | After Copilot opens a pull request |
| `pr.reviewed` | After Copilot reviews a PR |

### How to Create a Hook

**`post-edit.yml` — Run ESLint after every file Copilot edits:**

```yaml
# .github/hooks/post-edit.yml

name: lint-after-edit
on: file.after_write

# Only activate for these file types
filters:
  paths:
    - "**/*.ts"
    - "**/*.tsx"

steps:
  - name: Run ESLint
    run: npx eslint --fix "${{ event.file.path }}"
    
  - name: Report results
    if: steps.lint.exit_code != 0
    copilot_message: |
      ESLint found issues in `{{ event.file.path }}` that couldn't be auto-fixed.
      Please review the remaining errors before committing.
```

**`pre-tool-call.yml` — Block dangerous MCP tool calls:**

```yaml
# .github/hooks/pre-tool-call.yml

name: guard-destructive-tools
on: tool.before_call

filters:
  tools:
    - "database/*"
    - "filesystem/delete"

steps:
  - name: Require confirmation
    confirm:
      message: "Copilot wants to call `{{ event.tool.name }}` with these args: {{ event.tool.args | json }}. Allow?"
      options:
        - label: "Allow once"
          action: proceed
        - label: "Block"
          action: abort
          message: "Tool call blocked by user"
```

**`post-pr-open.yml` — Notify Slack when Copilot opens a PR:**

```yaml
# .github/hooks/post-pr-open.yml

name: slack-notify-on-pr
on: pr.opened

steps:
  - name: Post to Slack
    uses: slack/notify@v2
    with:
      webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      message: |
        🤖 Copilot opened a new PR: *{{ event.pr.title }}*
        {{ event.pr.url }}
```

### How to Run / Test Hooks

Hooks fire automatically during Copilot agent sessions. To test locally:

```bash
# Simulate a hook event using the Copilot CLI (if available)
gh copilot hooks test post-edit --file src/utils/format.ts

# View hook execution logs
gh copilot hooks logs --session <session-id>
```

---

## 7. ⚡ Agentic Workflows

### What is an Agentic Workflow?

An **agentic workflow** is a **GitHub Action written in Markdown** (`.md`) instead of YAML. The workflow's steps are described in natural language — Copilot interprets the intent and executes the appropriate tools and code.

This bridges the gap between "I know what I want to automate" and "I know how to write GitHub Actions YAML."

### Folder Structure

```
.github/workflows/
├── standard-ci.yml              # Regular GitHub Action (YAML)
├── agentic-code-review.md       # Agentic workflow (Markdown)
├── agentic-release-notes.md     # Agentic workflow (Markdown)
└── agentic-dependency-audit.md  # Agentic workflow (Markdown)
```

### How to Create an Agentic Workflow

Agentic workflows use **Markdown front-matter** to define triggers (same as GitHub Actions), then describe steps in plain English.

**`agentic-code-review.md` — AI-powered PR review:**

```markdown
---
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write
  contents: read
---

# Automated Code Review

## Context
You are reviewing a pull request in a TypeScript monorepo.
The repo uses React on the frontend and Node.js/Express on the backend.

## Steps

### 1. Understand the change
Read all changed files in this pull request. Identify:
- The purpose of the change
- Which packages/modules are affected
- Whether this is a feature, fix, refactor, or chore

### 2. Security review
Check for these security issues in the changed files:
- Hardcoded secrets, tokens, or passwords
- SQL injection vulnerabilities
- Unsanitized user input passed to dangerous functions
- Insecure use of `eval()`, `innerHTML`, or similar

If any are found, post a blocking review comment with the exact line and a recommended fix.

### 3. Code quality review
Evaluate the changes for:
- Functions longer than 40 lines (suggest splitting)
- Cyclomatic complexity above 10 (flag for simplification)
- Missing error handling in async functions
- Test coverage — are new code paths covered by tests?

### 4. Post review summary
Post a PR review comment with:
- A 2-sentence summary of what the PR does
- A "✅ Approved", "⚠️ Approved with suggestions", or "❌ Changes requested" verdict
- A bullet list of specific findings (if any)
```

**`agentic-release-notes.md` — Generate changelog from commits:**

```markdown
---
name: Generate Release Notes
on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
---

# Auto-Generate Release Notes

## Steps

### 1. Collect commits
Get all commits between the previous tag and this new tag.
Group them by conventional commit type: feat, fix, chore, docs, refactor.

### 2. Write release notes
Write human-friendly release notes in this format:

```
## What's New in {{ tag }}

### ✨ Features
- [Short description of each feat commit]

### 🐛 Bug Fixes
- [Short description of each fix commit]

### 🔧 Internal Changes
- [Grouped summary of chores/refactors — don't list every commit]
```

### 3. Publish
Create a GitHub Release with the generated notes attached to the current tag.
```

### How to Run an Agentic Workflow

Agentic workflows run exactly like standard GitHub Actions — they're triggered automatically by the events in the front-matter.

```bash
# Trigger manually via GitHub CLI
gh workflow run agentic-code-review.md

# Trigger manually via GitHub UI
# Go to: Actions → AI Code Review → Run workflow

# Watch it run
gh run watch
```

---

## 8. 🍳 Cookbook

### What is the Cookbook?

The **Cookbook** is a collection of **copy-paste-ready recipes** — small, self-contained code snippets and configurations for common Copilot API tasks. Each recipe solves one specific problem.

### Folder Structure

```
cookbook/
├── api/
│   ├── basic-completion.md
│   ├── streaming-response.md
│   ├── multi-turn-conversation.md
│   └── tool-use.md
├── agents/
│   ├── mcp-with-github.md
│   └── stateful-agent-session.md
├── integrations/
│   ├── copilot-in-vscode-extension.md
│   └── copilot-in-web-app.md
└── patterns/
    ├── rag-with-codebase.md
    └── prompt-chaining.md
```

### How to Create a Recipe

Each recipe is a Markdown file following this template:

````markdown
---
title: Stream a Copilot completion in Node.js
category: api
difficulty: beginner
tags: [streaming, node, typescript]
---

# Stream a Copilot Completion in Node.js

## Problem
You want to display Copilot's response token-by-token as it arrives, 
rather than waiting for the full response.

## Solution

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function streamCompletion(userMessage: string) {
  const stream = await client.messages.stream({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: userMessage }],
  });

  for await (const chunk of stream) {
    if (
      chunk.type === "content_block_delta" &&
      chunk.delta.type === "text_delta"
    ) {
      process.stdout.write(chunk.delta.text);
    }
  }

  const finalMessage = await stream.finalMessage();
  console.log("\n\nDone. Total tokens:", finalMessage.usage.output_tokens);
}

streamCompletion("Explain how React reconciliation works");
```

## How to Run

```bash
npm install @anthropic-ai/sdk
npx tsx recipe.ts
```

## Notes
- `stream.finalMessage()` gives you usage stats and stop reason after the stream ends
- For Express/Fastify, pipe the stream to `res` using `stream.on('text', ...)`

## See Also
- [Multi-turn conversation recipe](./multi-turn-conversation.md)
- [Tool use recipe](./tool-use.md)
````

### How to Use the Cookbook

Recipes are plain Markdown — copy the code block into your project.

```bash
# Browse all recipes
ls .github/cookbook/**/*.md

# Open a specific recipe
cat .github/cookbook/api/streaming-response.md

# Reference a recipe from Copilot Chat
@copilot Use the pattern from cookbook/patterns/rag-with-codebase.md to add search to our docs site
```

---

## 9. How All Components Work Together

Here's a complete picture of how the components interact during a real developer session:

```
Developer opens VS Code in the repo
           │
           ▼
   copilot-instructions.md ──────────────────► Always active, sets global context
           │
           ▼
Developer types: @api-agent scaffold a CRUD API for a "Product" resource
           │
           ▼
  PLUGIN resolves @api-agent ◄── plugin.yml maps agent name to agent folder
           │
           ▼
  AGENT loads system-prompt.md + registered SKILLS
           │
           ├──► INSTRUCTIONS auto-applied to *.ts files being generated
           │
           ├──► SKILL: api-scaffolder ──► runs generate-spec.py script
           │
           ▼
  Agent begins writing files...
           │
           ▼
  HOOK: file.after_write fires ──► runs ESLint --fix on each file
           │
           ▼
  Agent opens a Pull Request
           │
           ▼
  HOOK: pr.opened fires ──► posts Slack notification
           │
           ▼
  AGENTIC WORKFLOW: agentic-code-review.md triggers on PR
           │
           ▼
  AI reads diff, posts structured review comment
           │
           ▼
  Developer consults COOKBOOK for how to integrate the new API client
```

### Quick Reference Cheat Sheet

| Component | File location | Trigger | Purpose |
|---|---|---|---|
| Global instructions | `.github/copilot-instructions.md` | Always | Workspace-wide Copilot context |
| Instructions | `.github/copilot/instructions/*.md` | File pattern match | Per-filetype coding standards |
| Agent | `.github/copilot/agents/*/agent.yml` | `@agent-name` | Specialized AI persona |
| Skill | `.github/copilot/skills/*/SKILL.md` | Referenced by agent | Reusable AI procedure |
| Plugin | `.github/copilot/plugins/*/plugin.yml` | Enabled in settings | Bundle of agents + skills |
| Hook | `.github/hooks/*.yml` | Session lifecycle event | Middleware / automation |
| Agentic Workflow | `.github/workflows/*.md` | GitHub event (same as Actions) | AI-powered CI/CD |
| Cookbook | `cookbook/**/*.md` | Manual copy-paste | Ready-made API recipes |

---

*Generated for the GitHub Copilot Customization Repository — March 2026*