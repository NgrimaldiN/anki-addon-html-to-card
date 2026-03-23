from __future__ import annotations


LLM_GENERATION_GUIDANCE = (
    "LLM guidance: Default to a native-looking Anki Basic card unless the user "
    "explicitly asks for a more designed or unusual visual result. By default, "
    "omit note_type so the bundle uses the note type currently selected in Anki "
    "Add Cards. Keep the content compatible with Anki's stock Front/Back behavior "
    "and minimal styling unless the user explicitly asks for more design. If the "
    "user wants something more distinctive, you may return fully custom HTML/CSS, "
    "additional fields, richer layouts, and more original visual design. Only "
    "include note_type when custom fields, templates, or CSS are actually needed."
)


EXAMPLE_BUNDLE_TEXT = """{
  "version": 1,
  "notes": [
    {
      "fields": {
        "Front": "Write the question, term, or prompt here.",
        "Back": "Write the answer or explanation here.",
        "Extra": "Optional detail, nuance, mnemonic, or example."
      },
      "tags": ["llm", "example"]
    }
  ]
}"""
