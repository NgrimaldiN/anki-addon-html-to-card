from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from addon.errors import BundleValidationError


@dataclass(frozen=True)
class TemplateSpec:
    name: str
    qfmt: str
    afmt: str


@dataclass(frozen=True)
class NoteTypeSpec:
    name: str
    fields: list[str]
    templates: list[TemplateSpec]
    css: str
    reuse_existing: bool = True


@dataclass(frozen=True)
class NoteSpec:
    fields: dict[str, str]
    tags: list[str]


@dataclass(frozen=True)
class CardBundle:
    version: int
    note_type: NoteTypeSpec | None
    notes: list[NoteSpec]


_TOP_LEVEL_KEYS = {"version", "note_type", "notes"}
_NOTE_TYPE_KEYS = {"name", "fields", "templates", "css", "reuse_existing"}
_TEMPLATE_KEYS = {"name", "qfmt", "afmt"}
_NOTE_KEYS = {"fields", "tags"}


def normalize_bundle(payload: dict[str, Any]) -> CardBundle:
    _ensure_dict(payload, "Bundle root")
    _reject_unknown_keys(payload, _TOP_LEVEL_KEYS, "top-level")

    notes_payload = payload.get("notes")
    if not isinstance(notes_payload, list) or not notes_payload:
        raise BundleValidationError("The bundle must include a non-empty 'notes' list.")

    note_type = _normalize_note_type(payload.get("note_type"))
    notes = [
        _normalize_note(note_payload, note_index=index + 1)
        for index, note_payload in enumerate(notes_payload)
    ]

    if note_type is not None:
        allowed_fields = set(note_type.fields)
        for index, note in enumerate(notes, start=1):
            unknown_fields = sorted(set(note.fields) - allowed_fields)
            if unknown_fields:
                rendered_fields = ", ".join(unknown_fields)
                raise BundleValidationError(
                    f"Note {index} uses unknown fields for note type '{note_type.name}': "
                    f"{rendered_fields}"
                )

    version = payload.get("version", 1)
    if not isinstance(version, int):
        raise BundleValidationError("The bundle 'version' must be an integer.")

    return CardBundle(version=version, note_type=note_type, notes=notes)


def _normalize_note_type(payload: Any) -> NoteTypeSpec | None:
    if payload is None:
        return None
    _ensure_dict(payload, "'note_type'")
    _reject_unknown_keys(payload, _NOTE_TYPE_KEYS, "'note_type'")

    name = _require_string(payload.get("name"), "'note_type.name'")
    fields = _require_string_list(payload.get("fields"), "'note_type.fields'")
    if len(fields) != len(set(fields)):
        raise BundleValidationError("The note type field list contains duplicate names.")

    templates_payload = payload.get("templates")
    if not isinstance(templates_payload, list) or not templates_payload:
        raise BundleValidationError(
            "The bundle note type must include a non-empty 'templates' list."
        )

    templates = [_normalize_template(item, index + 1) for index, item in enumerate(templates_payload)]
    css = payload.get("css", "")
    if not isinstance(css, str):
        raise BundleValidationError("The bundle 'note_type.css' value must be a string.")

    reuse_existing = payload.get("reuse_existing", True)
    if not isinstance(reuse_existing, bool):
        raise BundleValidationError(
            "The bundle 'note_type.reuse_existing' value must be a boolean."
        )

    return NoteTypeSpec(
        name=name,
        fields=fields,
        templates=templates,
        css=css,
        reuse_existing=reuse_existing,
    )


def _normalize_template(payload: Any, index: int) -> TemplateSpec:
    _ensure_dict(payload, f"'note_type.templates[{index}]'")
    _reject_unknown_keys(payload, _TEMPLATE_KEYS, f"'note_type.templates[{index}]'")
    return TemplateSpec(
        name=_require_string(payload.get("name"), f"'note_type.templates[{index}].name'"),
        qfmt=_require_string(payload.get("qfmt"), f"'note_type.templates[{index}].qfmt'"),
        afmt=_require_string(payload.get("afmt"), f"'note_type.templates[{index}].afmt'"),
    )


def _normalize_note(payload: Any, note_index: int) -> NoteSpec:
    _ensure_dict(payload, f"'notes[{note_index}]'")
    _reject_unknown_keys(payload, _NOTE_KEYS, f"'notes[{note_index}]'")

    fields_payload = payload.get("fields")
    if not isinstance(fields_payload, dict) or not fields_payload:
        raise BundleValidationError(f"Note {note_index} must include a non-empty 'fields' object.")
    fields: dict[str, str] = {}
    for key, value in fields_payload.items():
        if not isinstance(key, str) or not key:
            raise BundleValidationError(f"Note {note_index} contains an invalid field name.")
        if not isinstance(value, str):
            raise BundleValidationError(
                f"Note {note_index} field '{key}' must contain a string value."
            )
        fields[key] = value

    tags_payload = payload.get("tags", [])
    tags = _require_string_list(
        tags_payload,
        f"'notes[{note_index}].tags'",
        allow_empty=True,
    )

    return NoteSpec(fields=fields, tags=tags)


def _reject_unknown_keys(payload: dict[str, Any], allowed: set[str], scope: str) -> None:
    unknown_keys = sorted(set(payload) - allowed)
    if unknown_keys:
        raise BundleValidationError(f"Unknown {scope} key: {unknown_keys[0]}")


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise BundleValidationError(f"The bundle {label} value must be a non-empty string.")
    return value


def _require_string_list(value: Any, label: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise BundleValidationError(f"The bundle {label} value must be a list of strings.")
    if not allow_empty and not value:
        raise BundleValidationError(f"The bundle {label} value must be a non-empty list of strings.")
    if any(not isinstance(item, str) or not item for item in value):
        raise BundleValidationError(f"The bundle {label} value must be a list of non-empty strings.")
    return list(value)


def _ensure_dict(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise BundleValidationError(f"{label} must be a JSON object.")
