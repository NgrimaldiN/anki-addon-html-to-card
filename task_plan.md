# Task Plan

## Goal

Research and plan an Anki add-on that adds a button to the Add Cards window, lets the user paste LLM-generated card bundle code/data, and creates one or many notes directly in the currently selected deck without using Anki import flows.

## Phases

| Phase | Status | Notes |
|---|---|---|
| 1. Set up planning artifacts | complete | Planning files and repo-local research notes created |
| 2. Research Anki APIs and patterns | complete | Official docs/source reviewed for hooks, models, decks, and packaging |
| 3. Define add-on architecture and input format | complete | JSON bundle format and module layout implemented |
| 4. Implement and validate | complete | Add-on, tests, docs, and syntax validation finished |

## Open Questions

- `add_cards_did_init` is the preferred Add Cards hook.
- The first version should accept JSON bundles only.
- Custom note type creation or update should happen only when the bundle explicitly includes `note_type`.
- The implementation should keep Anki imports isolated to the UI layer so pure modules stay testable in a plain Python environment.

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| Local shell cannot import `aqt` or `anki` modules | 1 | Switch to primary-source web research and local Anki profile inspection |
