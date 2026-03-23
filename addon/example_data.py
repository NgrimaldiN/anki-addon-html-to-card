from __future__ import annotations


LLM_GENERATION_GUIDANCE = (
    "LLM guidance: Default to a native-looking Anki Basic card unless the user "
    "explicitly asks for a more designed or unusual visual result. By default, "
    "keep the template close to Anki's stock Front/Back behavior, centered "
    "layout, and minimal styling. If the user wants something more distinctive, "
    "you may return fully custom HTML/CSS, additional fields, richer layouts, "
    "and more original visual design."
)


EXAMPLE_BUNDLE_TEXT = """{
  "version": 1,
  "note_type": {
    "name": "LLM Basic",
    "fields": ["Front", "Back", "Extra"],
    "templates": [
      {
        "name": "Card 1",
        "qfmt": "{{Front}}",
        "afmt": "{{FrontSide}}\\n\\n<hr id=answer>\\n\\n{{Back}}{{#Extra}}\\n\\n<div class='extra'>{{Extra}}</div>{{/Extra}}"
      }
    ],
    "css": ".card {\\n  font-family: arial;\\n  font-size: 20px;\\n  line-height: 1.5;\\n  text-align: center;\\n  color: black;\\n  background-color: white;\\n}\\n.extra {\\n  margin-top: 0.75em;\\n  color: #555;\\n  font-size: 0.9em;\\n}"
  },
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
