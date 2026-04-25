# AI Development Tool — Overview

An AI-powered development assistant that works seamlessly across **5 surfaces**, providing deep code intelligence, autonomous capabilities, and extensibility at every layer of your workflow.

---

## 5 Surfaces

| Surface | Description |
|---------|-------------|
| **CLI** | Terminal-first interface for scripting, automation, and headless workflows |
| **VS Code** | Native extension with inline completions, chat panel, and agent mode |
| **JetBrains** | Plugin for IntelliJ, PyCharm, WebStorm, GoLand, and all JetBrains IDEs |
| **Desktop** | Standalone native app for OS-level integration and persistent sessions |
| **Web** | Browser-based access for collaboration, code review, and lightweight tasks |

---

## Core Capabilities

### Context-Aware Codebase Understanding

- Indexes the entire repository to understand project structure, imports, and relationships
- Maintains context across files, functions, and modules
- Remembers prior conversation turns and code edits within a session
- Understands framework conventions, naming patterns, and project-specific idioms

---

### Autonomous, Collaborative, and Multi-Agent Modes

**Autonomous Mode**
- Executes multi-step tasks end-to-end with minimal human input
- Plans, implements, tests, and iterates independently

**Collaborative Mode**
- Works alongside the developer, suggesting and explaining at each step
- Human approves or adjusts actions before they are applied

**Multi-Agent Mode**
- Spawns specialized sub-agents for parallel task execution
- Agents share context and coordinate through a shared memory layer
- Supports orchestrator → worker hierarchies for complex pipelines

---

### Multi-Language Support with LSP Code Intelligence

- Full support for all major programming languages (Python, TypeScript, JavaScript, Go, Rust, Java, C#, C++, Ruby, and more)
- Powered by **Language Server Protocol (LSP)** for:
  - Accurate symbol resolution and go-to-definition
  - Cross-file reference tracking
  - Type-aware completions and refactoring
  - Syntax-correct code generation grounded in real AST data
- Language-specific best practices and idioms applied automatically

---

### Integrated Git Operations

- Read and reason over `git diff`, `git log`, and branch history
- Generate conventional commit messages from staged changes
- Summarize pull request changes and suggest reviewers
- Detect regressions by comparing against previous commits
- Create branches, stash changes, and manage merge conflicts

---

### Extensibility: Skills, Plugins, MCP, Hooks

| Extension Point | Purpose |
|----------------|---------|
| **Skills** | Packaged domain knowledge loaded on demand (e.g., testing, security, cloud) |
| **Plugins** | First- and third-party integrations that add new tools and surfaces |
| **MCP (Model Context Protocol)** | Open protocol for connecting external tools, APIs, and data sources to the AI |
| **Hooks** | Event-driven triggers that run custom logic before or after AI actions |

> Skills and MCP servers can be combined to give the agent access to live data, internal APIs, and specialized reasoning without modifying the core model.

---

## Summary

| Feature | Status |
|---------|--------|
| CLI surface | ✅ |
| VS Code surface | ✅ |
| JetBrains surface | ✅ |
| Desktop surface | ✅ |
| Web surface | ✅ |
| Context-aware codebase understanding | ✅ |
| Autonomous mode | ✅ |
| Collaborative mode | ✅ |
| Multi-agent mode | ✅ |
| Multi-language + LSP intelligence | ✅ |
| Integrated git operations | ✅ |
| Skills extensibility | ✅ |
| Plugin system | ✅ |
| MCP integration | ✅ |
| Hooks system | ✅ |
