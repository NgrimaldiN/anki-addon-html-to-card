# Findings

## Research Log

- The project workspace started empty, so the add-on will be scaffolded from scratch.
- The shell environment does not have importable `aqt` or `anki` Python modules, so direct local API introspection is unavailable.
- A local Anki profile exists at `/Users/ines/Library/Application Support/Anki2`, which confirms the target app is in use even though its Python packages are not exposed to this shell.
- Official current Anki source shows `AddCards.__init__()` calling `gui_hooks.add_cards_did_init(self)` after the dialog form, choosers, editor, note, and buttons are initialized.
- Official current `AddCards` members relevant to this project include `form.buttonBox`, `editor`, `deck_chooser`, and `notetype_chooser`.
- Official current hook definitions include `add_cards_did_init`, `add_cards_will_add_note`, `add_cards_did_add_note`, `addcards_did_change_note_type`, `add_cards_did_change_deck`, `editor_did_init_buttons`, and `editor_did_load_note`.
- Official current collection API includes `Collection.new_note(notetype)`, `Collection.add_note(note, deck_id)`, and `Collection.add_notes(requests)`.
- Official current bulk add request type is `anki.collection.AddNoteRequest(note=..., deck_id=...)`.
- Official current model manager API includes `col.models.by_name(name)`, `new(name)`, `add(notetype)`, `update_dict(notetype)`, `field_names(notetype)`, `new_field(name)`, `add_field(notetype, field)`, `new_template(name)`, `add_template(notetype, template)`, and `save(notetype)`.
- Packaging research indicates the minimum real add-on layout is a folder with `__init__.py` at the root. `manifest.json` is optional unless distributing a `.ankiaddon` outside AnkiWeb.
- Security research strongly favors a structured JSON bundle over executing pasted LLM-generated code inside Anki.
- Official current chooser APIs expose `deck_chooser.selected_deck_id` and `notetype_chooser.selected_notetype_id` as the preferred selected-target properties.
- Official current background mutation helper is `aqt.operations.CollectionOp`, which is appropriate for batch note insertion.

## Pending Research Areas

- Final implementation contract for the pasted bundle schema
