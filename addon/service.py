from __future__ import annotations

from addon.parser import parse_bundle_text
from addon.schema import CardBundle, normalize_bundle


def bundle_from_text(text: str) -> CardBundle:
    return normalize_bundle(parse_bundle_text(text))


def summarize_bundle(bundle: CardBundle) -> str:
    note_word = "note" if len(bundle.notes) == 1 else "notes"
    if bundle.note_type is None:
        return f"{len(bundle.notes)} {note_word} targeting the currently selected note type."
    return f"{len(bundle.notes)} {note_word} targeting custom note type '{bundle.note_type.name}'."
