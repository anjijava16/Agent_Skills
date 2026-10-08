---
name: dev-to-article-writer
description: Draft, structure, and refine developer-first technical articles, tutorials, and architecture breakdowns formatted specifically for the DEV.to community (DEV Community).
---

# DEV.to Technical Article Writer

Use this skill to draft, structure, and polish hands-on, code-first technical articles optimized specifically for the DEV.to platform, its Markdown parser, and its developer community.

## When to Use

- The user wants to write a DEV.to post from scratch, outline a tutorial, or share a developer experience story.
- The user asks to convert codebases, GitHub repositories, architecture diagrams, or engineering solutions into a DEV.to-ready post.

## DEV.to Formatting & Community Rules

1. **Front Matter & Tags:**
   - Always include standard DEV.to YAML front matter (`title`, `published`, `description`, `tags`, `cover_image`).
   - Limit tags to 4 max (e.g., `tags: ai, python, architecture, devops`). Use lowercase without `#`.

2. **Liquid Tags & Interactive Embeds:**
   - Use native DEV.to Liquid tags for code embeds and links where applicable:
     - GitHub Repo: `{% github user/repo %}`
     - CodePen: `{% codepen url %}`
     - Twitter/X: `{% twitter tweet_id %}`
     - Generic Link Cards: `{% embed url %}`

3. **Code-First Visual Scannability:**
   - **Code Blocks:** Specify exact language syntax highlighting (e.g., ```python, ```typescript, ```bash).
   - **Short Paragraphs:** Keep blocks to 2–4 sentences max.
   - **Gifs/Screenshots:** Include alt text and captions for accessibility (`![Alt text](url)`).
   - **Callout Blocks:** Use Blockquotes (`>`) for pro-tips, key warnings, or performance benchmarks.

4. **Tone & Community Mindset:**
   - Write in an approachable, peer-to-peer tone ("Here's what broke, here's how I fixed it, here's the full code").
   - Value pragmatism over overly formal corporate prose. Share trade-offs, setup gotchas, and real-world failure modes.

## Execution Workflow

1. **Alignment & Strategy:**
   - Identify the main problem solved, language/framework stack, and target audience level (Beginner, Intermediate, Advanced).

2. **DEV.to-Optimized Structure:**
   - **The Problem / Hook:** What failed or why the existing approach is frustrating.
   - **The Architecture / Concept:** High-level explanation with short code or diagram previews.
   - **The Implementation:** Step-by-step code blocks with inline comments.
   - **The Benchmarks / Verification:** How to test it locally or verify performance.
   - **Discussion Callout:** End with an open-ended question to spark discussion in the DEV.to comments section.

3. **Drafting:**
   - Write complete, copy-pasteable code examples with clear file paths in comments (e.g., `# src/router.py`).
