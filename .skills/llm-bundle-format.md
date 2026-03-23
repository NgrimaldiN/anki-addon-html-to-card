# LLM Bundle Format

## Recommendation

Accept structured JSON, not executable pasted code.

This keeps the add-on aligned with Anki’s official collection/model APIs and avoids introducing an unsafe `exec` path inside the desktop app.

## Accepted Input Forms

- Raw JSON
- A fenced Markdown code block whose contents are JSON

## Proposed Bundle Shape

```json
{
  "version": 1,
  "note_type": {
    "name": "Beautiful Basic",
    "reuse_existing": true,
    "fields": ["Front", "Back", "Extra"],
    "templates": [
      {
        "name": "Card 1",
        "qfmt": "<section class='hero'>{{Front}}</section>",
        "afmt": "{{FrontSide}}<hr id='answer'><section class='answer'>{{Back}}</section>{{#Extra}}<aside>{{Extra}}</aside>{{/Extra}}"
      }
    ],
    "css": ".card { font-family: Arial; }"
  },
  "notes": [
    {
      "fields": {
        "Front": "<h1>Question</h1>",
        "Back": "<p>Answer</p>",
        "Extra": "<small>Extra context</small>"
      },
      "tags": ["llm", "generated"]
    }
  ]
}
```

## Semantics

- `note_type` is optional.
- If `note_type` is omitted, use the note type currently selected in Add Cards.
- All imported notes go into the deck currently selected in Add Cards.
- The bundle does not choose or create a deck.
- Rich HTML inside fields is allowed.
- CSS and templates are allowed when a custom note type is supplied.

## Validation Rules

- Require top-level `notes`.
- Reject unknown top-level keys.
- Require each note to provide `fields`.
- If `note_type` is supplied, require `name`, `fields`, and `templates`.
- Require every note field name to exist in the active note type.
- Normalize missing optional `tags` to an empty list.
- Reject duplicate field names in note type definitions.
- Reject empty template lists.

## JavaScript Policy

- Do not execute pasted Python or JavaScript in the add-on itself.
- If users place JavaScript inside card templates, treat it as advanced opt-in content that Anki may render on cards, but document that Anki’s manual considers card-template JavaScript fragile and unsupported across clients.

## UX Notes

- The paste dialog should include a short example payload.
- On import, show how many notes were created and whether a note type was created or updated.
- Validation errors should point to the failing key or note index.

## Primary Sources

- https://docs.ankiweb.net/addons.html
- https://docs.ankiweb.net/templates/styling.html
- https://docs.ankiweb.net/templates/fields.html
- https://docs.ankiweb.net/editing.html
- https://github.com/ankitects/anki/security
- https://addon-docs.ankiweb.net/addon-config.html
- https://addon-docs.ankiweb.net/background-ops.html
