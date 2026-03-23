# Task Plan

## Goal

Research and plan an Anki add-on that adds a button to the Add Cards window, lets the user paste LLM-generated card bundle code/data, and creates one or many notes directly in the currently selected deck without using Anki import flows.

## Phases

| Phase | Status | Notes |
|---|---|---|
| 1. Set up planning artifacts | complete | Planning files and repo-local research notes created |
| 2. Research Anki APIs and patterns | complete | Official docs/source reviewed for hooks, models, decks, and packaging |
| 3. Define add-on architecture and input format | in_progress | JSON bundle format and module layout drafted |
| 4. Implement and validate | pending | Code starts after the research plan is accepted or complete |

## Open Questions

- `add_cards_did_init` is the preferred Add Cards hook.
- The first version should accept JSON bundles only.
- Custom note type creation or update should happen only when the bundle explicitly includes `note_type`.

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| Local shell cannot import `aqt` or `anki` modules | 1 | Switch to primary-source web research and local Anki profile inspection |
