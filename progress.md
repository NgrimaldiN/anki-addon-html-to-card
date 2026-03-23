# Progress

## 2026-03-23

- Initialized the repository-level planning files for a research-first workflow.
- Verified the workspace is empty and not a git repository.
- Confirmed `pytest` is available locally for later test-driven implementation work.
- Confirmed local imports for `aqt` and `anki` are unavailable in this shell, so planning will rely on primary sources and defensive integration code.
- Spawned five parallel Anki-focused research agents to cover hooks/UI insertion, collection/model APIs, packaging, safety, and Add Cards state.
- Pulled official current source from `ankitects/anki` via GitHub API to inspect `qt/aqt/addcards.py`, `qt/tools/genhooks_gui.py`, `pylib/anki/models.py`, `pylib/anki/collection.py`, and `qt/aqt/operations/note.py`.
- Confirmed from upstream source that `add_cards_did_init` is the correct dialog-level hook for adding a custom button to the Add Cards window.
- Confirmed from upstream source that non-blocking note insertion can use `aqt.operations.note.add_note(parent=..., note=..., target_deck_id=...)`.
- Confirmed from upstream source that bulk note insertion can use `CollectionOp(parent, lambda col: col.add_notes([...AddNoteRequest(...) ...]))`.
- Added repo-local knowledge files in `.skills/` and `.agent/` to preserve the Anki-specific guidance and planned module structure.
