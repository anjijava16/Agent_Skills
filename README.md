# Agent Skills

A collection of [Agent Skills](https://agentskills.io/home) — portable instruction packages that give AI agents new capabilities.

## Available Skills

| Skill | Description |
|-------|-------------|
| `pdf-processing` | Extract text, tables, and metadata from PDFs with OCR fallback |
| `data-analysis` | Explore, clean, transform, and visualize datasets (CSV, Excel, JSON) |
| `code-review` | Review code for bugs, security vulnerabilities, performance, and style |
| `pdf-service` | Fill PDF forms, merge, split, and convert PDFs |
| `roll-dice` | Generate random dice rolls using standard NdX notation (e.g. 2d6, 1d20) |
| `analyze-csv-files` | Load, inspect, filter, sort, aggregate, and clean CSV/TSV files |
| `csv-analyzer-workspace` | Evaluate and benchmark CSV analysis quality with evalsets and grading |
| `my-skill` | Template skill (customize for your use case) |

## How to Use

Agent Skills aren't run directly. They're loaded automatically by compatible agents (VS Code Copilot, Claude Code, etc.).

### 1. Place skills where the agent can find them

Copy or symlink a skill into your project's skill directory:

```bash
# VS Code (GitHub Copilot)
mkdir -p /path/to/project/.agents/skills
cp -r pdf-service /path/to/project/.agents/skills/

# Claude Code
mkdir -p /path/to/project/.claude/skills
cp -r pdf-service /path/to/project/.claude/skills/

# Or symlink (keeps skills in one place)
ln -s "$(pwd)/pdf-service" /path/to/project/.agents/skills/pdf-service
```

| Agent | Default Skill Location |
|-------|----------------------|
| VS Code (Copilot) | `.agents/skills/` in project root |
| Claude Code | `.claude/skills/` or `~/.claude/skills/` (global) |

### 2. Activate Agent mode

In VS Code Copilot Chat, select **Agent mode** from the mode dropdown at the bottom of the chat panel.

### 3. Verify discovery

Type `/skills` in the chat panel — your skill should appear in the list.

### 4. Use it naturally

Ask a question that matches the skill's description. The agent activates the skill automatically:

```
"Extract text from invoice.pdf"
"Merge these three PDFs into one"
"Fill out the form fields in application.pdf"
```

## How It Works

1. **Discovery** — Agent reads only `name` + `description` from all skills at startup (~100 tokens each)
2. **Activation** — Your prompt matches the description → agent loads the full `SKILL.md` into context
3. **Execution** — Agent follows the instructions, runs code, and loads `references/` or `scripts/` only when needed

## Skill Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + markdown instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed documentation (loaded on demand)
└── assets/           # Optional: templates, resources
```

## References

- [Agent Skills Spec](https://agentskills.io/specification)
- [Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Best Practices](https://agentskills.io/skill-creation/best-practices)
- [Example Skills (GitHub)](https://github.com/anthropics/skills)

## Public Skills & Community Resources

Free, open-source skills you can install directly into your projects.

### Official Repositories

| Repository | Stars | Description |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 105k | Official Anthropic skills — webapp-testing, MCP builder, PDF, XLSX, PPTX, document skills |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | 14.4k | The Agent Skills specification, documentation, and reference SDK |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | - | Community instructions, agents, and skills for GitHub Copilot |

### Curated Skill Collections

| Repository | Description |
|---|---|
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ skills from official dev teams and community — code review, testing, and more |
| [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | 5,400+ skills filtered and categorized from the OpenClaw registry |
| [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | 1,326+ installable skills with CLI installer — code review, git hooks, and more |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Curated skills, hooks, slash-commands, and agent orchestrators |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Curated list of Claude skills, resources, and tools |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 192+ skills — engineering, marketing, product, compliance, C-level advisory |

### Code Review & Development Skills

| Repository | Description |
|---|---|
| [gitstq/awesome-ai-agent-skills](https://github.com/gitstq/awesome-ai-agent-skills) | 4 production-grade skills including **Code Review Engine** + self-improving memory |
| [vickhunter/pr-rules-sync](https://github.com/vickhunter/pr-rules-sync) | Scans merged PRs to auto-extract code review rules as a reusable skill |

### Domain-Specific Skills

| Repository | Description |
|---|---|
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Research, science, engineering, analysis, finance, and writing |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | 100+ product management skills — discovery, strategy, execution, launch, growth |

### Skill Builders & Platforms

| Repository | Description |
|---|---|
| [refly-ai/refly](https://github.com/refly-ai/refly) | Open-source agent skills builder — define skills by vibe workflow, run on Claude Code, Cursor, Codex |

### Browse All

- **GitHub Topic**: [github.com/topics/agent-skills](https://github.com/topics/agent-skills) — **2,212+ public repositories** and growing
- **Discord Community**: [discord.gg/MKPE9g8aUy](https://discord.gg/MKPE9g8aUy) — discuss skills with the community

### How to Install a Public Skill

```bash
# Clone and copy into your project
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/webapp-testing .agents/skills/

# Or clone an entire collection
git clone https://github.com/VoltAgent/awesome-agent-skills.git /tmp/awesome-skills
cp -r /tmp/awesome-skills/skills/code-review .agents/skills/

# Or symlink for easy updates
ln -s /path/to/cloned/skill .agents/skills/skill-name
```

> **Note**: There are no dedicated standalone "java-code-review" or "python-code-review" skills published yet. The general code-review skills in the collections above work for all languages. For language-specific patterns, create your own skill using `my-skill/` as a template.

---

# 🧠 Agent vs Skills vs Tools — Complete Deep Dive (Beginner → Advanced → Expert)

---

# 🚀 1. Introduction

Modern AI systems like GitHub Copilot, Claude Code, and agent frameworks are built using three core building blocks:

* 🧠 **Agent (Brain)**
* 📦 **Skills (Instructions / Capability Modules)**
* 🛠 **Tools (Execution Layer)**

Understanding how these interact is the key to building powerful AI systems.

---

# 🧩 2. High-Level Mental Model

```text
User Request
     ↓
🧠 Main Agent (Reasoning + Planning)
     ↓
📦 Skills (Guidance + Workflows)
     ↓
🛠 Tools (Execution)
     ↓
Result
```

---

# 🧠 3. What is an Agent?

An **Agent** is the core intelligence system.

### Responsibilities:

* Understand user intent
* Plan multi-step tasks
* Decide what to do next
* Use tools
* Iterate until completion

---

## 🔁 Agent Core Loop (ReAct Pattern)

```text
THINK → PLAN → ACT → OBSERVE → REFINE → REPEAT
```

---

## ✅ Agent Capabilities

* Reasoning
* Planning
* Decision-making
* Tool selection
* Error handling

---

## ❗ Important

> There is usually **ONE main agent**, not many.

---

# 📦 4. What are Skills?

A **Skill** is a reusable capability module that helps the agent perform specific types of tasks.

---

## 📁 Skill Structure

```text
skill-name/
├── SKILL.md
├── scripts/
├── assets/
```

---

## 🧠 What SKILL.md Contains

* Instructions
* Best practices
* Workflows
* When to use the skill

---

## ✅ Skill Properties

* Passive (does not act on its own)
* Used by agent when needed
* Provides domain expertise

---

## ❗ Key Insight

> Skills guide **HOW to think**, not **WHAT to execute**

---

# 🛠 5. What are Tools?

Tools are executable functions/APIs.

---

## Examples

* Run tests
* Read files
* Call APIs
* Execute scripts

---

## Tool Characteristics

* Perform real actions
* Return results
* No intelligence

---

# ⚖️ 6. Skills vs Tools vs Agents

| Feature  | Skills       | Tools     | Agents       |
| -------- | ------------ | --------- | ------------ |
| Purpose  | Guidance     | Execution | Intelligence |
| Active   | ❌            | ❌         | ✅            |
| Think    | ❌            | ❌         | ✅            |
| Execute  | ⚠️ via agent | ✅         | ✅            |
| Autonomy | ❌            | ❌         | ✅            |

---

# 🔄 7. How Everything Works Together

### Example: "Fix auth bug"

---

## Step 1: Agent Understands Task

* Debugging
* Backend issue

---

## Step 2: Agent Selects Skills

* debugging skill
* backend skill

---

## Step 3: Agent Plans

```text
- Run tests
- Identify failure
- Fix code
```

---

## Step 4: Agent Uses Tools

* run_tests
* open_file
* apply_patch

---

## Step 5: Agent Iterates Until Done

---

# 🧠 8. Why Skills Exist (Industry Perspective)

Companies focus on skills instead of agents because:

---

## 1️⃣ Standardization

Skills are easy to define:

```text
name + description + instructions
```

Agents are complex:

* loops
* memory
* orchestration

---

## 2️⃣ Portability

Skills work across platforms
Agents do not

---

## 3️⃣ Safety

Skills:

* Passive
* Controlled by agent

Agents:

* Autonomous
* Hard to control

---

## 4️⃣ Simplicity

Skills:

* Easy to build
* Easy to share

Agents:

* Hard to debug
* Complex systems

---

## 5️⃣ Platform Control

Companies want to control:

* Intelligence layer
* Reasoning engine

So they expose:

* Skills ✅
* Tools ✅
* Agents ❌

---

# 🧩 9. Skill Folder vs Agent Folder

---

## 📦 Skill Folder

```text
skills/pdf-processing/
├── SKILL.md
└── scripts/extract.py
```

### Behavior:

* Passive
* Used by main agent
* No independent thinking

---

## 🤖 Agent Folder

```text
agents/pdf_agent/
├── AGENT.md
├── memory.json
└── scripts/extract.py
```

---

## Agent Capabilities:

* Own reasoning loop
* Own planning
* Independent execution

---

# ⚠️ Key Difference

| Concept | Meaning                |
| ------- | ---------------------- |
| Skill   | "Tell me how to do it" |
| Agent   | "You do it yourself"   |

---

# 🔁 10. Sequential vs Parallel Execution

---

## 🧠 Agent Thinking

Always **sequential**

```text
Step-by-step reasoning
```

---

## ⚡ Execution Layer

Can be **parallel**

Examples:

* Multiple file analysis
* Running tests + linting
* Code review across files

---

## 🧠 Key Insight

> Parallelism happens in execution, not thinking

---

# 🧩 11. Why It Feels Like Multiple Agents

Because system can:

* Use multiple skills
* Run multiple tools
* Process multiple files

---

But actually:

> Still ONE agent orchestrating everything

---

# 🏗️ 12. Advanced Architecture

---

## Single-Agent System

```text
Agent → Skills → Tools
```

---

## Multi-Agent System

```text
Main Agent (Orchestrator)
     ↓
Specialized Agents
     ↓
Tools
```

---

# 🤖 13. Converting Skill → Agent

---

## Skill (Before)

```text
- Instructions only
- No autonomy
```

---

## Agent (After)

```text
- Has AGENT.md
- Has reasoning loop
- Executes independently
```

---

## Key Additions

* Thinking loop
* Planning ability
* Tool control
* Memory (optional)

---

# 🧠 14. Deep Insight (Critical)

---

## Skills = Capability Expansion

They increase what agent *can do*

---

## Agents = Intelligence Distribution

They distribute *decision-making*

---

# 🚀 15. Real Industry Pattern

```text
User
 ↓
Main Agent (central brain)
 ↓
Skills (plugins)
 ↓
Tools (execution)
```

---

# ❗ Why Not Multiple Agents Everywhere?

Problems:

* Coordination complexity
* Infinite loops
* Debugging difficulty
* Performance overhead

---

# 🔮 16. Future Direction

* Hybrid systems (skills + agents)
* Controlled multi-agent orchestration
* Skill marketplaces
* Agent platforms

---

# 🧠 17. Final Mental Model

---

## 🧠 Agent

> The brain (decision-maker)

---

## 📦 Skills

> The knowledge (how to think)

---

## 🛠 Tools

> The hands (how to act)

---

# 🎯 Final Takeaway

* You are always working with **ONE main agent**
* Skills help the agent **think better**
* Tools help the agent **act**
* Agents (advanced) allow **delegation and scaling**

---

# 🏁 From Beginner → Hero

### Beginner:

* Understand tools

### Intermediate:

* Use skills effectively

### Advanced:

* Design agent workflows

### Expert:

* Build multi-agent systems

---

# 🚀 You Are Here

👉 Moving from **Advanced → Expert (Agent Architect)**

---
