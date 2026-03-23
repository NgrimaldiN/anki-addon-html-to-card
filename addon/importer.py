from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from addon.errors import BundleValidationError
from addon.schema import CardBundle, NoteTypeSpec


@dataclass(frozen=True)
class PendingAddNoteRequest:
    note: Any
    deck_id: int


@dataclass(frozen=True)
class ImportSummary:
    note_count: int
    deck_id: int
    note_type_name: str
    created_note_type: bool
    updated_note_type: bool
    note_type_id: Any
    changes: Any | None = None


def import_bundle(
    *,
    collection: Any,
    bundle: CardBundle,
    selected_notetype_id: Any,
    selected_deck_id: Any,
    request_factory: Callable[..., Any] = PendingAddNoteRequest,
) -> ImportSummary:
    note_type, created_note_type, updated_note_type = _resolve_note_type(
        collection=collection,
        bundle=bundle,
        selected_notetype_id=selected_notetype_id,
    )

    field_names = collection.models.field_names(note_type)
    requests = []
    for note_index, note_spec in enumerate(bundle.notes, start=1):
        unknown_fields = sorted(set(note_spec.fields) - set(field_names))
        if unknown_fields:
            rendered_fields = ", ".join(unknown_fields)
            raise BundleValidationError(
                f"Note {note_index} uses unknown fields for note type "
                f"'{note_type['name']}': {rendered_fields}"
            )

        note = collection.new_note(note_type)
        for field_name, value in note_spec.fields.items():
            note[field_name] = value
        note.tags = list(note_spec.tags)
        requests.append(request_factory(note=note, deck_id=selected_deck_id))

    changes = collection.add_notes(requests)

    return ImportSummary(
        note_count=len(requests),
        deck_id=selected_deck_id,
        note_type_name=note_type["name"],
        created_note_type=created_note_type,
        updated_note_type=updated_note_type,
        note_type_id=note_type["id"],
        changes=changes,
    )


def _resolve_note_type(
    *,
    collection: Any,
    bundle: CardBundle,
    selected_notetype_id: Any,
) -> tuple[Any, bool, bool]:
    if bundle.note_type is None:
        note_type = collection.models.get(selected_notetype_id)
        if note_type is None:
            raise BundleValidationError("The selected Add Cards note type could not be found.")
        return note_type, False, False

    spec = bundle.note_type
    existing = collection.models.by_name(spec.name) if spec.reuse_existing else None
    if existing is not None:
        if _note_type_matches_spec(collection.models, existing, spec):
            return existing, False, False
        _apply_note_type_spec(collection.models, existing, spec)
        collection.models.update_dict(existing)
        return existing, False, True

    new_note_type = collection.models.new(spec.name)
    _apply_note_type_spec(collection.models, new_note_type, spec)
    collection.models.add(new_note_type)
    return new_note_type, True, False


def _apply_note_type_spec(models: Any, note_type: Any, spec: NoteTypeSpec) -> None:
    note_type["name"] = spec.name
    note_type["css"] = spec.css
    note_type["flds"] = []
    note_type["tmpls"] = []

    for field_name in spec.fields:
        field = models.new_field(field_name)
        models.add_field(note_type, field)

    for template_spec in spec.templates:
        template = models.new_template(template_spec.name)
        template["qfmt"] = template_spec.qfmt
        template["afmt"] = template_spec.afmt
        models.add_template(note_type, template)


def _note_type_matches_spec(models: Any, note_type: Any, spec: NoteTypeSpec) -> bool:
    if note_type["name"] != spec.name:
        return False
    if note_type.get("css", "") != spec.css:
        return False
    if models.field_names(note_type) != spec.fields:
        return False

    existing_templates = note_type.get("tmpls", [])
    if len(existing_templates) != len(spec.templates):
        return False

    for existing, expected in zip(existing_templates, spec.templates):
        if existing.get("name") != expected.name:
            return False
        if existing.get("qfmt", "") != expected.qfmt:
            return False
        if existing.get("afmt", "") != expected.afmt:
            return False

    return True
