---

## name: medium-article-writer
description: Write, draft, outline, or refine high-engagement technical and thought-leadership articles formatted specifically for Medium. Use when converting code, architecture, or tech topics into publication-ready Medium drafts.

# Medium Article Writer

Use this skill to create, structure, and refine long-form technical or thought-leadership articles optimized specifically for Medium's editor constraints and audience reading habits.

## When to Use

* The user wants to write a Medium article from scratch, outline an idea, or draft a technical post.
* The user asks to convert a README, technical document, architecture spec, GitHub repo, or code concept into a publication-ready Medium draft.

## Medium Formatting & Constraints Rules

1. **Visual Scannability:**
* **No Markdown Tables:** Medium does not native-render Markdown tables (`| header | header |`). Convert tabular data into key-value bulleted lists, bolded attribute comparisons, or structured code/JSON blocks.
* **Hero Image Placeholder:** Always place a wide hero image placeholder at the top of the article directly below the main title/subtitle.
* **Paragraph Length:** Keep paragraphs short (2–4 sentences max) to improve readability on mobile devices.
* **Bold Lead-ins:** Use bolded text prefixes for bullet points to enable rapid scanning for readers.
* **Header Hierarchy:** Strictly use H1 (`#`) for Title, H2 (`##`) for main section breaks, and H3 (`###`) for sub-sections.


2. **Engaging Structural Flow:**
* **The Hook:** Open with a strong first sentence that challenges an industry assumption, highlights a common developer pain point (e.g., late-night debugging, high API latency, schema exceptions), or presents an engineering contrast.
* **The Body:** Group logical concepts with H2 section breaks. Insert visual placeholders (e.g., `[Insert visual diagram showing X vs Y here]`) when text-heavy sections span longer than 3–4 paragraphs.
* **Code Blocks:** Keep code snippets clean, well-commented, and directly runnable or copy-pasteable.
* **The Takeaway:** End with actionable key takeaways or architectural conclusions rather than a generic summary.


3. **Tone and Voice:**
* Write in an authentic, conversational, engineer-to-engineer voice.
* Avoid generic AI clichés, overly academic prose, and repetitive transition words (e.g., "In conclusion," "Furthermore," "Moreover").



## Execution Workflow

1. **Alignment & Strategy:**
* Identify the primary technical topic, core thesis, key results, and target developer audience level (e.g., AI Engineers, Platform Architects).


2. **Structural Outline:**
* Map out the H2 section headings, visual/diagram locations, and code snippets before drafting.


3. **Medium-Optimized Drafting:**
* Write the full text adhering to Medium layout constraints (short paragraphs, no Markdown tables, bolded list items, visual placeholders).


4. **Polish & Final Review:**
* Eliminate passive voice, ensure crisp headers, and suggest catchy, non-clickbait titles.
