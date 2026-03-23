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
    "Only include note_type when custom fields, templates, or CSS are actually "
    "needed. Return only one JSON object, with no trailing semicolon, no extra "
    "wrapper braces, and no second object after it. CRITICAL JSON FORMATTING "
    "RULES: never place literal physical newlines, tabs, or other control "
    "characters inside JSON string values; keep each JSON string on one physical "
    "line and use escaped sequences like \\n or \\t when you need formatting. "
    "Escape every literal backslash inside JSON strings; for math or LaTeX-style "
    "commands, write \\\\gamma, \\\\pi, \\\\epsilon, etc., or prefer Unicode "
    "symbols like γ, π, ε."
)


EXAMPLE_BUNDLE_TEXT = """{
  // FORMAT EXAMPLE FOR ANOTHER LLM:
  // RETURN ONLY THIS JSON OBJECT (or one fenced ```json block) and nothing else.
  // No prose before or after the JSON. No trailing semicolon.
  // For maximum compatibility, switch Anki Add Cards to a working note type like "Basic"
  // before using this default format.
  // Default to the note type already selected in Anki Add Cards.
  // Omit "note_type" unless you truly need custom fields, templates, or CSS.
  "version": 1,
  "notes": [
    {
      "fields": {
        "Front": "Write the question, term, or prompt here.",
        // CRITICAL JSON FORMATTING RULE:
        // Keep every JSON string on a single physical line.
        // If you need a visual line break inside a value, write \\n instead of pressing Enter.
        // Escape every literal backslash inside JSON strings.
        // For math or LaTeX-style commands, write \\\\gamma, \\\\pi, \\\\epsilon, etc.,
        // or use Unicode symbols like γ, π, ε.
        "Back": "Write the answer or explanation here. Use \\\\n for intentional line breaks inside the string.",
        "Extra": "Optional detail, nuance, mnemonic, or example."
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
