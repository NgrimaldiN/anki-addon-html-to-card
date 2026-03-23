from __future__ import annotations


LLM_GENERATION_GUIDANCE = (
    "LLM guidance: Default to a native-looking Anki Basic card unless the user "
    "explicitly asks for a more designed or unusual visual result. By default, "
    "omit note_type so the bundle uses the note type currently selected in Anki "
    "Add Cards. Keep the content compatible with Anki's stock Front/Back behavior "
    "and minimal styling unless the user explicitly asks for more design. If the "
    "user wants something more distinctive, you may return fully custom HTML/CSS, "
    "additional fields, richer layouts, and more original visual design. Only "
    "include note_type when custom fields, templates, or CSS are actually needed. "
    "CRITICAL JSON FORMATTING RULE: never place literal physical newlines, tabs, or "
    "other control characters inside JSON string values; keep each JSON string on one "
    "physical line and use escaped sequences like \\n or \\t when you need formatting."
)


EXAMPLE_BUNDLE_TEXT = """{
  // FORMAT EXAMPLE FOR ANOTHER LLM:
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
  // Just keep the JSON structurally valid.
}"""
