# Anki Add-on API Notes

## Purpose

Local implementation notes for building an Anki add-on that augments the Add Cards window and imports one or many LLM-generated notes directly into the currently selected deck.

## Packaging

- Minimum add-on layout: a folder with `__init__.py` at the root.
- `manifest.json` is optional for AnkiWeb distribution, but useful if packaging a `.ankiaddon` outside AnkiWeb.
- Do not store persistent user data in the add-on root because upgrades can overwrite it.

## Add Cards Integration

- Preferred dialog hook: `aqt.gui_hooks.add_cards_did_init`.
- The hook fires after the `AddCards` dialog has built its form, choosers, editor, current note, and buttons.
- Best insertion point for this project: add a `QPushButton` to `addcards.form.buttonBox` with `QDialogButtonBox.ButtonRole.ActionRole`.

## Relevant `AddCards` Surface

- `addcards.form.buttonBox`
- `addcards.editor`
- `addcards.deck_chooser.selected_deck_id`
- `addcards.notetype_chooser.selected_notetype_id`
- `addcards.set_deck(deck_id)`
- `addcards.set_note_type(notetype_id)`

## Note Creation Flow

1. Read the current target deck from `addcards.deck_chooser.selected_deck_id`.
2. Resolve the note type from `addcards.notetype_chooser.selected_notetype_id`, unless the pasted bundle requests a custom note type.
3. Build notes with `col.new_note(notetype)`.
4. Set field values with dict-style note access, such as `note["Front"] = "<div>...</div>"`.
5. Validate note content with `note.fields_check()`.
6. Add notes to the selected deck.

## Bulk Add Pattern

- Single note: `aqt.operations.note.add_note(parent=..., note=..., target_deck_id=...)`
- Many notes: use `aqt.operations.CollectionOp` with `col.add_notes([AddNoteRequest(...), ...])`
- Keep collection writes out of the UI thread.

## Note Type Creation / Update

- Lookup existing type: `col.models.by_name(name)`
- Create shell: `col.models.new(name)`
- Add field: `new_field()` then `add_field()`
- Add template: `new_template()` then `add_template()`
- Update or persist: `update_dict()` for existing types, `add()` or `add_dict()` for new types
- CSS lives on the note type dict as `notetype["css"]`

## Compatibility Guidance

- Prefer new-style `gui_hooks`.
- Prefer snake_case APIs.
- Avoid deprecated hook names like `add_cards_did_change_note_type`; use `addcards_did_change_note_type`.

## Primary Sources

- https://addon-docs.ankiweb.net/hooks-and-filters.html
- https://addon-docs.ankiweb.net/addon-folders.html
- https://addon-docs.ankiweb.net/sharing.html
- https://raw.githubusercontent.com/ankitects/anki/main/qt/aqt/addcards.py
- https://raw.githubusercontent.com/ankitects/anki/main/qt/tools/genhooks_gui.py
- https://raw.githubusercontent.com/ankitects/anki/main/qt/aqt/deckchooser.py
- https://raw.githubusercontent.com/ankitects/anki/main/qt/aqt/notetypechooser.py
- https://raw.githubusercontent.com/ankitects/anki/main/qt/aqt/operations/note.py
- https://raw.githubusercontent.com/ankitects/anki/main/pylib/anki/collection.py
- https://raw.githubusercontent.com/ankitects/anki/main/pylib/anki/models.py
