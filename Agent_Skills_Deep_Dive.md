# Agent Skills: A Deep Dive — From Beginner to Hero

> **Source**: [agentskills.io](https://agentskills.io/home) — the open standard for giving AI agents new capabilities.

---

## Table of Contents

1. [What Are Agent Skills?](#1-what-are-agent-skills)
2. [Why Do We Need Skills?](#2-why-do-we-need-skills)
3. [How Skills Work — The Three-Phase Lifecycle](#3-how-skills-work--the-three-phase-lifecycle)
4. [The SKILL.md File — Anatomy of a Skill](#4-the-skillmd-file--anatomy-of-a-skill)
5. [Specification Deep Dive](#5-specification-deep-dive)
6. [Creating Your First Skill (Quickstart)](#6-creating-your-first-skill-quickstart)
7. [Best Practices for Skill Authors](#7-best-practices-for-skill-authors)
8. [Optimizing Skill Descriptions](#8-optimizing-skill-descriptions)
9. [Bundling Scripts in Skills](#9-bundling-scripts-in-skills)
10. [Evaluating Skill Quality](#10-evaluating-skill-quality)
11. [Where Skills Are Installed](#11-where-skills-are-installed)
12. [Compatible Agents and Ecosystem](#12-compatible-agents-and-ecosystem)
13. [Advanced: How Agents Implement Skills Support](#13-advanced-how-agents-implement-skills-support)
14. [Real-World Examples](#14-real-world-examples)
15. [Summary Cheat Sheet](#15-summary-cheat-sheet)

---

## 1. What Are Agent Skills?

Agent Skills are **a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows**.

At its core, a skill is just a **folder** containing a `SKILL.md` file. That file includes metadata (a `name` and `description`, at minimum) and instructions that tell an agent how to perform a specific task. Skills can also bundle scripts, templates, and reference materials.

```
my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

Think of skills as **reusable knowledge packages** — they capture domain expertise, workflows, and tool-specific instructions so that agents can perform tasks more accurately and efficiently than relying on their general training alone.

### Key Properties

- **Self-documenting**: A human can read `SKILL.md` and understand exactly what the skill does
- **Extensible**: Skills can range from pure text instructions to full executable code
- **Portable**: Skills are just files — easy to edit, version, and share
- **Open standard**: Originally developed by Anthropic, now adopted across the ecosystem

---

## 2. Why Do We Need Skills?

AI agents are powerful, but they often lack the **specific context** they need:

| Problem | How Skills Solve It |
|---------|-------------------|
| Agents don't know your company's conventions | Skills encode project-specific rules and patterns |
| Agents hallucinate tool usage | Skills provide exact commands with correct flags |
| Agents miss edge cases | Gotchas sections capture non-obvious pitfalls |
| Workflows aren't repeatable | Skills define step-by-step procedures |
| Knowledge is scattered | Skills package it into portable units |

### Who Benefits?

- **Skill authors**: Build capabilities once and deploy them across multiple agent products
- **Compatible agents**: Support for skills lets end users give agents new capabilities out of the box
- **Teams and enterprises**: Capture organizational knowledge in portable, version-controlled packages

### What Can Skills Enable?

- **Domain expertise**: Legal review processes, data analysis pipelines, security auditing
- **New capabilities**: Creating presentations, building MCP servers, analyzing datasets
- **Repeatable workflows**: Multi-step tasks turned into consistent, auditable processes
- **Interoperability**: The same skill works across different skills-compatible agents

---

## 3. How Skills Work — The Three-Phase Lifecycle

Skills use **progressive disclosure** to manage context efficiently. The agent doesn't load everything upfront — it loads more information progressively as needed.

### Phase 1: Discovery (~100 tokens per skill)

At startup, the agent scans known skill directories and reads **only** the `name` and `description` from each `SKILL.md` frontmatter. This gives the agent a lightweight catalog of what's available.

```
[Agent starts]
  → Scans .agents/skills/
  → Finds: pdf-processing, data-analysis, code-review
  → Loads only name + description for each (~300 tokens total)
```

### Phase 2: Activation (<5000 tokens recommended)

When a user's task matches a skill's description, the agent loads the **full `SKILL.md` body** into context and follows its instructions.

```
[User asks: "Extract text from invoice.pdf"]
  → Agent matches against pdf-processing description
  → Loads full SKILL.md into context
  → Now has detailed instructions for handling PDFs
```

### Phase 3: Execution (as needed)

The agent follows the loaded instructions. If the instructions reference supporting files (scripts, references, assets), the agent loads them **only when needed**.

```
[Agent reads: "Run scripts/extract.py for OCR fallback"]
  → Loads scripts/extract.py
  → Executes it
  → Returns results to user
```

### Why This Matters

An agent with 50 installed skills doesn't pay the token cost of 50 full instruction sets upfront. It pays ~5,000 tokens for the catalog, then loads only the 1-2 skills actually needed per conversation. This keeps agents **fast and context-efficient**.

---

## 4. The SKILL.md File — Anatomy of a Skill

Every skill starts with a `SKILL.md` file containing **YAML frontmatter** and **Markdown instructions**.

### Basic Structure

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
---

# PDF Processing

## When to use this skill
Use this skill when the user needs to work with PDF files...

## How to extract text
1. Use pdfplumber for text extraction...

## How to fill forms
...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | **Yes** | Max 64 chars. Lowercase letters, numbers, hyphens only. Must match the folder name. |
| `description` | **Yes** | Max 1024 chars. What the skill does + when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements (tools, packages, network access). |
| `metadata` | No | Arbitrary key-value pairs (author, version, etc.). |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. (Experimental) |

### Minimal Example

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Full Example

```yaml
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
compatibility: Requires Python 3.10+ and poppler
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(python3:*) Read
---
```

### Body Content

The Markdown body after the frontmatter is where the real instructions live. There are **no format restrictions** — write whatever helps agents perform the task effectively.

**Recommended sections:**
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases (gotchas)
- Validation steps

---

## 5. Specification Deep Dive

### Name Field Rules

The `name` field has strict formatting requirements:

```
✅ Valid:
  pdf-processing
  data-analysis
  code-review

❌ Invalid:
  PDF-Processing      # uppercase not allowed
  -pdf                # cannot start with hyphen
  pdf--processing     # consecutive hyphens not allowed
  my skill            # spaces not allowed
```

**Critical rule**: The `name` must match the parent directory name. If your folder is `pdf-processing/`, the name must be `pdf-processing`.

### Description Field Guidelines

The description carries the **entire burden of triggering**. If the agent can't tell from the description that the skill is relevant, it won't load it.

```yaml
# ❌ Poor — too vague
description: Helps with PDFs.

# ✅ Good — specific about what and when
description: >
  Extracts text and tables from PDF files, fills PDF forms,
  and merges multiple PDFs. Use when working with PDF documents
  or when the user mentions PDFs, forms, or document extraction.
```

### Optional Directories

#### `scripts/`

Contains executable code that agents can run. Scripts should:
- Be self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully
- Avoid interactive prompts (agents run in non-interactive shells)
- Prefer structured output (JSON/CSV) over free-form text

#### `references/`

Contains additional documentation loaded on demand:
- `REFERENCE.md` — Detailed technical reference
- Domain-specific files (`finance.md`, `legal.md`, etc.)

Keep individual reference files **focused and small** — agents load these on demand, so smaller files mean less use of context.

#### `assets/`

Contains static resources:
- Templates (document templates, configuration templates)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)

### Progressive Disclosure Numbers

| Tier | What | When Loaded | Token Budget |
|------|------|-------------|-------------|
| Metadata | `name` + `description` | Session start | ~50-100 per skill |
| Instructions | Full `SKILL.md` body | Skill activated | <5000 recommended |
| Resources | Scripts, references, assets | As referenced | Varies |

**Guideline**: Keep `SKILL.md` under **500 lines**. Move detailed reference material to separate files.

### File References

Use relative paths from the skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

Keep file references **one level deep** from `SKILL.md`. Avoid deeply nested reference chains.

---

## 6. Creating Your First Skill (Quickstart)

Let's build a simple dice-rolling skill step by step.

### Step 1: Create the Directory

VS Code looks for skills in `.agents/skills/` by default:

```bash
mkdir -p .agents/skills/roll-dice
```

### Step 2: Write SKILL.md

Create `.agents/skills/roll-dice/SKILL.md`:

```markdown
---
name: roll-dice
description: >
  Roll dice using a random number generator. Use when asked to
  roll a die (d6, d20, etc.), roll dice, or generate a random dice roll.
---

To roll a die, use the following command that generates a random
number from 1 to the given number of sides:

```bash
echo $((RANDOM % <sides> + 1))
```

Replace `<sides>` with the number of sides on the die (e.g., 6
for a standard die, 20 for a d20).
```

That's it — **one file, under 20 lines**.

### Step 3: Test It

1. Open your project in VS Code
2. Open the Copilot Chat panel
3. Select **Agent mode** from the dropdown
4. Type `/skills` to confirm `roll-dice` appears
5. Ask: *"Roll a d20"*

The agent should activate the skill, run the terminal command, and return a random number between 1 and 20.

> **Note**: Tool-use reliability varies across models. If the agent responds without running a terminal command, try a different model.

---

## 7. Best Practices for Skill Authors

### Start from Real Expertise

A common pitfall is asking an LLM to generate a skill without providing domain-specific context. The result is vague, generic procedures. Effective skills are grounded in real expertise.

#### Extract from a Hands-On Task

Complete a real task in conversation with an agent, providing context, corrections, and preferences. Then extract the reusable pattern into a skill. Pay attention to:

- **Steps that worked** — the sequence of actions that led to success
- **Corrections you made** — places where you steered the agent
- **Input/output formats** — what the data looked like going in and coming out
- **Context you provided** — project-specific facts and constraints

#### Synthesize from Existing Artifacts

Good source material includes:
- Internal documentation, runbooks, style guides
- API specifications, schemas, configuration files
- Code review comments and issue trackers
- Version control history (especially patches and fixes)
- Real-world failure cases and their resolutions

### Refine with Real Execution

The first draft usually needs refinement. Run the skill against real tasks, then feed the results back. Ask:
- What triggered false positives?
- What was missed?
- What could be cut?

> **Tip**: Read agent execution traces, not just final outputs. If the agent wastes time on unproductive steps, the instructions may be too vague, too broad, or presenting too many options without a clear default.

### Spending Context Wisely

Every token in your skill competes for the agent's attention with everything else in the context window.

#### Add What the Agent Lacks, Omit What It Knows

```markdown
<!-- ❌ Too verbose — the agent already knows what PDFs are -->
## Extract PDF text
PDF (Portable Document Format) files are a common file format that contains
text, images, and other content...

<!-- ✅ Better — jumps straight to what the agent wouldn't know -->
## Extract PDF text
Use pdfplumber for text extraction. For scanned documents, fall back to
pdf2image with pytesseract.
```

**Ask yourself**: "Would the agent get this wrong without this instruction?" If no, cut it.

#### Design Coherent Units

Scope skills like functions — encapsulate a coherent unit of work:
- **Too narrow**: Multiple skills load for a single task, risking conflicts
- **Too broad**: Hard to activate precisely
- **Just right**: A skill for querying a database and formatting results

#### Aim for Moderate Detail

Overly comprehensive skills can hurt more than they help. Concise, stepwise guidance with a working example tends to outperform exhaustive documentation.

### Calibrating Control

#### Match Specificity to Fragility

**Give freedom** when multiple approaches are valid:
```markdown
## Code review process
1. Check all database queries for SQL injection
2. Verify authentication checks on every endpoint
3. Look for race conditions in concurrent code paths
```

**Be prescriptive** when operations are fragile:
```markdown
## Database migration
Run exactly this sequence:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
```

#### Provide Defaults, Not Menus

```markdown
<!-- ❌ Too many equal options -->
You can use pypdf, pdfplumber, PyMuPDF, or pdf2image...

<!-- ✅ Clear default with escape hatch -->
Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

#### Favor Procedures Over Declarations

```markdown
<!-- ❌ Specific answer — only useful for this exact task -->
Join the orders table to customers on customer_id...

<!-- ✅ Reusable method — works for any query -->
1. Read the schema from references/schema.yaml
2. Join tables using the _id foreign key convention
3. Apply filters from the user's request as WHERE clauses
4. Aggregate numeric columns as needed
```

---

## 8. Optimizing Skill Descriptions

The `description` field is the **single most important piece** of a skill because it determines whether the skill gets activated at all.

### How Triggering Works

Agents only consult skills for tasks that require knowledge beyond what they can handle alone. A simple "read this file" may not trigger a skill even if the description matches, because the agent can handle it with basic tools.

### Writing Effective Descriptions

| Principle | Example |
|-----------|---------|
| Use imperative phrasing | "Use this skill when…" not "This skill does…" |
| Focus on user intent | Describe what the user wants, not implementation |
| Be pushy | List contexts explicitly, including non-obvious ones |
| Keep it concise | A few sentences to a short paragraph |

```yaml
# ❌ Before
description: Process CSV files.

# ✅ After
description: >
  Analyze CSV and tabular data files — compute summary statistics,
  add derived columns, generate charts, and clean messy data. Use this
  skill when the user has a CSV, TSV, or Excel file and wants to
  explore, transform, or visualize the data, even if they don't
  explicitly mention "CSV" or "analysis."
```

### Testing Trigger Accuracy

Create evaluation queries in `eval_queries.json`:

```json
[
  {
    "query": "I've got a spreadsheet with revenue in col C — can you add a profit margin column?",
    "should_trigger": true
  },
  {
    "query": "convert this json to yaml",
    "should_trigger": false
  }
]
```

Aim for ~20 queries: 8-10 should-trigger, 8-10 should-not-trigger.

**Should-trigger tips**: Vary phrasing (formal/casual), explicitness (direct/indirect), detail level, and complexity.

**Should-not-trigger tips**: Use near-misses that share keywords but need something different (these are the most valuable negative test cases).

### The Optimization Loop

1. Evaluate the current description on train + validation sets
2. Identify failures in the **train set only**
3. Revise (generalize, don't overfit to specific failed queries)
4. Repeat until results stabilize (~5 iterations)
5. Pick the iteration with the best **validation** pass rate

---

## 9. Bundling Scripts in Skills

### One-Off Commands (No scripts/ needed)

When an existing package does what you need, reference it directly:

```markdown
## Lint the codebase
```bash
uvx ruff@0.8.0 check .
```
```

**Pin versions** so the command behaves the same over time.

### Self-Contained Scripts

For reusable logic, bundle scripts that declare their own dependencies inline.

**Python (PEP 723)**:
```python
# /// script
# dependencies = [
#   "beautifulsoup4>=4.12,<5",
# ]
# ///

from bs4 import BeautifulSoup
# ...
```

Run with: `uv run scripts/extract.py`

### Referencing Scripts from SKILL.md

```markdown
## Available scripts

- **`scripts/validate.sh`** — Validates configuration files
- **`scripts/process.py`** — Processes input data

## Workflow

1. Run the validation script:
   ```bash
   bash scripts/validate.sh "$INPUT_FILE"
   ```
```

### Designing Scripts for Agents

| Guideline | Why |
|-----------|-----|
| **No interactive prompts** | Agents can't respond to TTY prompts — the script will hang |
| **Document with `--help`** | Primary way the agent learns your script's interface |
| **Helpful error messages** | "Error: --format must be json, csv, or table. Received: xml" |
| **Structured output** | JSON/CSV over free-form text; data to stdout, diagnostics to stderr |
| **Idempotent operations** | Agents may retry — "create if not exists" is safer |
| **`--dry-run` support** | Lets agents preview destructive operations |
| **Meaningful exit codes** | Different codes for different failure types |
| **Predictable output size** | Cap output or use pagination to avoid context truncation |

---

## 10. Evaluating Skill Quality

### Design Test Cases

A test case has three parts: **prompt**, **expected output**, and optional **input files**.

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "prompt": "Find the top 3 months by revenue in data/sales_2025.csv and make a bar chart",
      "expected_output": "A bar chart showing the top 3 months by revenue",
      "files": ["evals/files/sales_2025.csv"],
      "assertions": [
        "The output includes a bar chart image file",
        "The chart shows exactly 3 months",
        "Both axes are labeled"
      ]
    }
  ]
}
```

### Run Evals (With vs. Without)

Run each test case **twice**: once with the skill and once without. This gives you a baseline to compare against.

```
csv-analyzer-workspace/
└── iteration-1/
    ├── eval-top-months-chart/
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   ├── timing.json
    │   │   └── grading.json
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── benchmark.json
```

### Write Good Assertions

```
✅ Good:
  "The output file is valid JSON"
  "The bar chart has labeled axes"
  "The report includes at least 3 recommendations"

❌ Weak:
  "The output is good"
  "The output uses exactly the phrase 'Total Revenue: $X'"
```

### Grade and Aggregate

```json
{
  "run_summary": {
    "with_skill": { "pass_rate": { "mean": 0.83 } },
    "without_skill": { "pass_rate": { "mean": 0.33 } },
    "delta": { "pass_rate": 0.50 }
  }
}
```

A skill that improves pass rate by 50 percentage points while adding 13 seconds is probably worth it. A skill that doubles tokens for a 2-point improvement might not be.

### The Iteration Loop

1. Give eval signals + current `SKILL.md` to an LLM → propose improvements
2. Review and apply changes
3. Rerun all test cases in a new `iteration-N+1/` directory
4. Grade and aggregate
5. Human review → repeat

Stop when feedback is consistently empty or improvements plateau.

---

## 11. Where Skills Are Installed

### Standard Locations

| Scope | Path | Purpose |
|-------|------|---------|
| Project (cross-client) | `<project>/.agents/skills/` | Shared across all compatible agents |
| Project (VS Code) | `<project>/.agents/skills/` | VS Code Copilot native |
| Project (Claude Code) | `<project>/.claude/skills/` | Claude Code native |
| User (cross-client) | `~/.agents/skills/` | Available in all projects |
| User (Claude Code) | `~/.claude/skills/` | Claude Code global |

### Precedence Rules

- **Project-level** skills override **user-level** skills with the same name
- Within the same scope, first-found or last-found (implementation-dependent)
- Collisions generate a warning so users know a skill was shadowed

### Trust Considerations

Project-level skills come from the repository, which may be untrusted (e.g., a cloned open-source project). Some agents gate project-level skill loading on a trust check to prevent untrusted repos from injecting instructions.

---

## 12. Compatible Agents and Ecosystem

Agent Skills are supported by a growing list of AI development tools:

| Agent | Status |
|-------|--------|
| Claude Code | Supported |
| VS Code (GitHub Copilot) | Supported |
| Amp | Supported |
| TRAE | Supported |
| OpenHands | Supported |
| Piebald | Supported |
| OpenCode | Supported |
| Snowflake Cortex | Supported |
| Spring AI | Supported |
| Qodo | Supported |
| Laravel Boost | Supported |
| Mistral AI Vibe | Supported |

The standard is open to contributions. Discussion happens on [GitHub](https://github.com/agentskills/agentskills) and [Discord](https://discord.gg/MKPE9g8aUy).

---

## 13. Advanced: How Agents Implement Skills Support

If you're building an agent or tool that needs to support skills, here's the full integration lifecycle.

### Step 1: Discover Skills

At session startup, scan known directories for subdirectories containing `SKILL.md`:

```
~/.agents/skills/
├── pdf-processing/
│   ├── SKILL.md          ← discovered
│   └── scripts/
├── data-analysis/
│   └── SKILL.md          ← discovered
└── README.md             ← ignored
```

**Practical scanning rules:**
- Skip `.git/`, `node_modules/`
- Respect `.gitignore`
- Set depth bounds (max 4-6 levels, max 2000 directories)

### Step 2: Parse SKILL.md

Extract YAML frontmatter, validate, store in an in-memory map:

```python
# Minimum skill record:
{
    "name": "pdf-processing",
    "description": "Extract PDF text, fill forms...",
    "location": "/home/user/.agents/skills/pdf-processing/SKILL.md"
}
```

**Be lenient**: Warn on issues but still load the skill. Only skip if the description is empty or YAML is completely unparseable.

### Step 3: Disclose to the Model (Catalog)

Build a lightweight catalog in the system prompt or tool description:

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extract PDF text, fill forms, merge files.</description>
    <location>/home/user/.agents/skills/pdf-processing/SKILL.md</location>
  </skill>
</available_skills>
```

Include behavioral instructions:

```
The following skills provide specialized instructions for specific tasks.
When a task matches a skill's description, use your file-read tool to load
the SKILL.md at the listed location before proceeding.
```

### Step 4: Activate Skills

Two patterns for model-driven activation:

1. **File-read activation**: Model calls its file-read tool with the `SKILL.md` path. Simplest approach.
2. **Dedicated tool activation**: Register an `activate_skill` tool that returns formatted content. More control.

**Structured wrapping** (for dedicated tools):

```xml
<skill_content name="pdf-processing">
# PDF Processing
...
<skill_resources>
  <file>scripts/extract.py</file>
  <file>references/pdf-spec-summary.md</file>
</skill_resources>
</skill_content>
```

### Step 5: Manage Context Over Time

- **Protect skill content from pruning** — skill instructions are durable behavioral guidance
- **Deduplicate activations** — don't inject the same skill twice
- **Subagent delegation** (optional) — run complex skills in a separate session

---

## 14. Real-World Examples

### Example 1: Simple Command Skill

```markdown
---
name: roll-dice
description: Roll dice. Use when asked to roll a die (d6, d20, etc.).
---

# Roll Dice

```bash
echo $((RANDOM % <sides> + 1))
```

Replace `<sides>` with the number of sides.
```

### Example 2: Full Skill with Scripts and References

```
pdf-service/
├── SKILL.md                  # Core: extract, fill, merge, split
├── scripts/
│   └── extract_text.py       # Text extraction with OCR fallback
└── references/
    └── REFERENCE.md          # Advanced: watermarks, encryption, redaction
```

### Example 3: Skill with Validation Loop

```markdown
---
name: form-processor
description: Process and fill PDF forms. Use when filling PDF forms or processing form data.
---

## Workflow

Progress:
- [ ] Step 1: Analyze the form (`scripts/analyze_form.py`)
- [ ] Step 2: Create field mapping (`fields.json`)
- [ ] Step 3: Validate mapping (`scripts/validate_fields.py`)
- [ ] Step 4: Fill the form (`scripts/fill_form.py`)
- [ ] Step 5: Verify output (`scripts/verify_output.py`)

## Validation
1. Make your edits
2. Run validation: `python scripts/validate.py output/`
3. If validation fails, fix and re-run
4. Only proceed when validation passes
```

---

## 15. Summary Cheat Sheet

### Skill File Quick Reference

```yaml
---
name: my-skill              # Required: lowercase, hyphens, matches folder name
description: >              # Required: what it does + when to use it
  Do X, Y, Z. Use when the user asks about A or B.
license: MIT                # Optional
compatibility: Python 3.10+ # Optional
metadata:                   # Optional
  author: your-name
  version: "1.0"
---

# Instructions go here (Markdown, no restrictions)
```

### Do's and Don'ts

| Do | Don't |
|----|-------|
| Keep SKILL.md under 500 lines | Write exhaustive documentation in SKILL.md |
| Use gotchas sections for non-obvious facts | Explain things the agent already knows |
| Provide a clear default tool/approach | Present equal options without a recommendation |
| Write procedures (how to approach) | Write declarations (what to produce for one case) |
| Test with varied, realistic prompts | Test with one prompt and call it done |
| Pin versions in script commands | Assume specific tool versions are installed |
| Use structured output (JSON/CSV) in scripts | Use free-form text output from scripts |

### Installation Commands

```bash
# Create a new skill
mkdir -p .agents/skills/my-skill

# Copy into a project
cp -r my-skill /path/to/project/.agents/skills/

# Symlink from a shared location
ln -s "$(pwd)/my-skill" /path/to/project/.agents/skills/my-skill

# Validate (using skills-ref)
skills-ref validate ./my-skill
```

### The Lifecycle in One Picture

```
[Agent starts]
     │
     ▼
  ┌──────────────────────────┐
  │  DISCOVERY               │  Read name + description
  │  (~100 tokens per skill) │  from all SKILL.md files
  └──────────┬───────────────┘
             │
  [User asks a question]
             │
             ▼
  ┌──────────────────────────┐
  │  ACTIVATION              │  Match prompt → description
  │  (<5000 tokens)          │  Load full SKILL.md body
  └──────────┬───────────────┘
             │
  [Agent follows instructions]
             │
             ▼
  ┌──────────────────────────┐
  │  EXECUTION               │  Run scripts, load references
  │  (as needed)             │  and assets on demand
  └──────────────────────────┘
             │
             ▼
       [Result to user]
```

---

## Further Reading

- **Specification**: [agentskills.io/specification](https://agentskills.io/specification)
- **Quickstart**: [agentskills.io/skill-creation/quickstart](https://agentskills.io/skill-creation/quickstart)
- **Best Practices**: [agentskills.io/skill-creation/best-practices](https://agentskills.io/skill-creation/best-practices)
- **Optimizing Descriptions**: [agentskills.io/skill-creation/optimizing-descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- **Evaluating Skills**: [agentskills.io/skill-creation/evaluating-skills](https://agentskills.io/skill-creation/evaluating-skills)
- **Using Scripts**: [agentskills.io/skill-creation/using-scripts](https://agentskills.io/skill-creation/using-scripts)
- **Adding Skills Support**: [agentskills.io/client-implementation/adding-skills-support](https://agentskills.io/client-implementation/adding-skills-support)
- **Example Skills on GitHub**: [github.com/anthropics/skills](https://github.com/anthropics/skills)
- **Agent Skills GitHub**: [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills)
- **Discord Community**: [discord.gg/MKPE9g8aUy](https://discord.gg/MKPE9g8aUy)
