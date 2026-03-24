from __future__ import annotations


LLM_GENERATION_GUIDANCE = (
    "LLM guidance: Return only one fenced json block or one raw JSON object, with "
    "no prose before or after it. Default to a native-looking Anki Basic card "
    "unless the user explicitly asks for a more designed or unusual visual result. "
    "By default, omit note_type so the bundle uses the note type currently selected "
    "in Anki Add Cards, but use that default only when the selected note type is "
    "already a working note type such as Basic. If you omit note_type, select "
    "Anki's working 'Basic' note type first, or another known-good note type, "
    "before importing. Keep the content compatible with Anki's stock Front/Back "
    "behavior and minimal styling unless the user explicitly asks for more design. "
    "If the user wants something more distinctive, you may return fully custom "
    "HTML/CSS, additional fields, richer layouts, and more original visual design. "
    "If you use Extra, any field beyond Front/Back, custom templates, or custom "
    "CSS, include a complete note_type block so the cards work immediately when "
    "imported. Return only one JSON object, with no trailing semicolon, no extra "
    "wrapper braces, and no second object after it. CRITICAL JSON FORMATTING "
    "RULES: never place literal physical newlines, tabs, or other control "
    "characters inside JSON string values; keep each JSON string on one physical "
    "line and use escaped sequences like \\n or \\t when you need formatting. "
    "For math, use normal LaTeX/MathJax-style notation such as $V^\\\\pi(s)$, "
    "$\\\\gamma$, $\\\\epsilon$, $\\\\mathbb{E}[X]$, or $\\\\mathbb{P}(A)$. "
    "Do not drop commands like \\\\mathbb{E} or \\\\mathbb{P} when you want "
    "blackboard-bold symbols. "
    "Because this is JSON, escape every literal backslash inside JSON strings."
)


EXAMPLE_BUNDLE_TEXT = """{
  // FORMAT EXAMPLE FOR ANOTHER LLM:
  // RETURN ONLY THIS JSON OBJECT (or one fenced ```json block) and nothing else.
  // No prose before or after the JSON. No trailing semicolon.
  // For maximum compatibility, switch Anki Add Cards to a working note type like "Basic"
  // before using this default format.
  // Default to the note type already selected in Anki Add Cards.
  // Omit "note_type" only when you want a plain Basic-style card with existing fields.
  // If you want "Extra", any new field, or custom HTML/CSS, include a full "note_type" block instead.
  "version": 1,
  "notes": [
    {
      "fields": {
        "Front": "Write the question, term, or prompt here.",
        // CRITICAL JSON FORMATTING RULE:
        // Keep every JSON string on a single physical line.
        // If you need a visual line break inside a value, write \\n instead of pressing Enter.
        // For math, use normal LaTeX/MathJax-style notation like $V^\\\\pi(s)$, $\\\\gamma$,
        // $\\\\mathbb{E}[X]$, or $\\\\mathbb{P}(A)$.
        // Do not forget commands like \\\\mathbb{E} or \\\\mathbb{P} when you want those symbols.
        // Because this is JSON, escape every literal backslash inside string values.
        "Back": "Write the answer or explanation here. Use \\\\n for intentional line breaks inside the string."
      },
      "tags": ["llm", "example"]
    }
  ]

  // You are free to be much more creative when the user asks for it:
  // - custom note_type
  // - fully custom HTML/CSS
  // - additional fields
  // - more original visual design
  // Prefer strict JSON in the final answer even though these comments explain the format.
}"""


CUSTOM_NOTE_TYPE_EXAMPLE_TEXT = """{
  // USE THIS SHAPE WHEN YOU WANT EXTRA FIELDS OR A MORE ORIGINAL CARD DESIGN.
  "version": 1,
  "note_type": {
    "name": "LLM Creative Basic",
    "fields": ["Front", "Back", "Extra"],
    "templates": [
      {
        "name": "Card 1",
        "qfmt": "<section class=\\"prompt\\">{{Front}}</section>",
        "afmt": "{{FrontSide}}<hr id=\\"answer\\"><section class=\\"answer\\">{{Back}}</section>{{#Extra}}<section class=\\"extra\\">{{Extra}}</section>{{/Extra}}"
      }
    ],
    "css": ".card { font-family: arial; font-size: 20px; text-align: center; color: black; background: white; } .extra { margin-top: 1em; color: #555; font-size: 0.9em; }",
    "reuse_existing": true
  },
  "notes": [
    {
      "fields": {
        "Front": "Write the question, term, or prompt here.",
        "Back": "Write the answer or explanation here. Use \\\\n for intentional line breaks inside the string.",
        "Extra": "Optional detail, nuance, mnemonic, or example."
      },
      "tags": ["llm", "example"]
    }
  ]
}"""


LLM_PROMPT_TEXT = f"""Generate Anki cards using the schema below.

Output rules:
- Return only one fenced ```json``` block.
- No prose before or after the JSON.
- No trailing semicolon.
- If you omit "note_type", assume Anki Add Cards is already set to a working note type such as "Basic".
- If you use "Extra", any field beyond "Front"/"Back", custom templates, or custom CSS, include a complete "note_type" block.
- If you want a super original card design, include a full "note_type" block so the cards work immediately on import.
- Keep every JSON string value on one physical line.
- Use \\n for line breaks inside string values.
- For math, use normal LaTeX/MathJax notation inside JSON strings, for example $V^\\\\pi(s)$, $\\\\gamma$, $\\\\epsilon$, $\\\\mathbb{{E}}[X]$, and $\\\\mathbb{{P}}(A)$.
- Do not forget commands like \\\\mathbb{{E}} and \\\\mathbb{{P}} when you want blackboard-bold expectation/probability symbols.
- Because this is JSON, escape every backslash inside string values.

Safe default example:
```jsonc
{EXAMPLE_BUNDLE_TEXT}
```

Custom note_type example:
```jsonc
{CUSTOM_NOTE_TYPE_EXAMPLE_TEXT}
```"""
