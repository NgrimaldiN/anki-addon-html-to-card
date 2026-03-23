from __future__ import annotations

from dataclasses import dataclass

import pytest

from addon.errors import BundleValidationError
from addon.importer import import_bundle
from addon.schema import CardBundle, NoteSpec, NoteTypeSpec, TemplateSpec


@dataclass
class FakeAddNoteRequest:
    note: "FakeNote"
    deck_id: int


class FakeNote:
    def __init__(self, notetype: dict) -> None:
        self.notetype = notetype
        self.values = {field["name"]: "" for field in notetype["flds"]}
        self.tags: list[str] = []

    def __setitem__(self, key: str, value: str) -> None:
        if key not in self.values:
            raise KeyError(key)
        self.values[key] = value


class FakeModels:
    def __init__(self, notetypes: list[dict]) -> None:
        self._notetypes = {item["id"]: item for item in notetypes}
        self._next_id = max(self._notetypes, default=0) + 1
        self.updated_ids: list[int] = []
        self.added_ids: list[int] = []

    def get(self, notetype_id: int) -> dict | None:
        return self._notetypes.get(notetype_id)

    def by_name(self, name: str) -> dict | None:
        for notetype in self._notetypes.values():
            if notetype["name"] == name:
                return notetype
        return None

    def new(self, name: str) -> dict:
        return {"id": 0, "name": name, "flds": [], "tmpls": [], "css": ""}

    def add(self, notetype: dict) -> dict:
        notetype["id"] = self._next_id
        self._next_id += 1
        self._notetypes[notetype["id"]] = notetype
        self.added_ids.append(notetype["id"])
        return notetype

    def update_dict(self, notetype: dict) -> dict:
        self._notetypes[notetype["id"]] = notetype
        self.updated_ids.append(notetype["id"])
        return notetype

    def field_names(self, notetype: dict) -> list[str]:
        return [field["name"] for field in notetype["flds"]]

    def new_field(self, name: str) -> dict:
        return {"name": name}

    def add_field(self, notetype: dict, field: dict) -> None:
        notetype["flds"].append(field)

    def new_template(self, name: str) -> dict:
        return {"name": name, "qfmt": "", "afmt": ""}

    def add_template(self, notetype: dict, template: dict) -> None:
        notetype["tmpls"].append(template)


class FakeCollection:
    def __init__(self, notetypes: list[dict]) -> None:
        self.models = FakeModels(notetypes)
        self.added_requests: list[FakeAddNoteRequest] = []

    def new_note(self, notetype: dict) -> FakeNote:
        return FakeNote(notetype)

    def add_notes(self, requests: list[FakeAddNoteRequest]) -> None:
        self.added_requests.extend(requests)


def test_import_bundle_uses_selected_note_type_and_selected_deck() -> None:
    collection = FakeCollection(
        [
            {
                "id": 42,
                "name": "Basic",
                "flds": [{"name": "Front"}, {"name": "Back"}],
                "tmpls": [{"name": "Card 1", "qfmt": "{{Front}}", "afmt": "{{Back}}"}],
                "css": "",
            }
        ]
    )
    bundle = CardBundle(
        version=1,
        note_type=None,
        notes=[
            NoteSpec(fields={"Front": "Q1", "Back": "A1"}, tags=["llm"]),
            NoteSpec(fields={"Front": "Q2", "Back": "A2"}, tags=[]),
        ],
    )

    summary = import_bundle(
        collection=collection,
        bundle=bundle,
        selected_notetype_id=42,
        selected_deck_id=100,
        request_factory=FakeAddNoteRequest,
    )

    assert summary.note_count == 2
    assert summary.note_type_name == "Basic"
    assert summary.created_note_type is False
    assert summary.updated_note_type is False
    assert [request.deck_id for request in collection.added_requests] == [100, 100]
    assert collection.added_requests[0].note.values == {"Front": "Q1", "Back": "A1"}
    assert collection.added_requests[0].note.tags == ["llm"]


def test_import_bundle_creates_new_note_type_from_bundle() -> None:
    collection = FakeCollection([])
    bundle = CardBundle(
        version=1,
        note_type=NoteTypeSpec(
            name="Beautiful Basic",
            fields=["Front", "Back", "Extra"],
            templates=[
                TemplateSpec(
                    name="Card 1",
                    qfmt="<section>{{Front}}</section>",
                    afmt="{{FrontSide}}<hr id=answer>{{Back}}",
                )
            ],
            css=".card { color: teal; }",
        ),
        notes=[NoteSpec(fields={"Front": "Q", "Back": "A", "Extra": "More"}, tags=[])],
    )

    summary = import_bundle(
        collection=collection,
        bundle=bundle,
        selected_notetype_id=42,
        selected_deck_id=100,
        request_factory=FakeAddNoteRequest,
    )

    created = collection.models.by_name("Beautiful Basic")
    assert created is not None
    assert summary.created_note_type is True
    assert summary.updated_note_type is False
    assert collection.models.field_names(created) == ["Front", "Back", "Extra"]
    assert created["tmpls"][0]["qfmt"] == "<section>{{Front}}</section>"
    assert created["css"] == ".card { color: teal; }"


def test_import_bundle_updates_existing_note_type_when_requested() -> None:
    collection = FakeCollection(
        [
            {
                "id": 7,
                "name": "Beautiful Basic",
                "flds": [{"name": "Front"}, {"name": "Back"}],
                "tmpls": [{"name": "Card 1", "qfmt": "{{Front}}", "afmt": "{{Back}}"}],
                "css": ".card { color: black; }",
            }
        ]
    )
    bundle = CardBundle(
        version=1,
        note_type=NoteTypeSpec(
            name="Beautiful Basic",
            fields=["Front", "Back", "Extra"],
            templates=[
                TemplateSpec(
                    name="Card 1",
                    qfmt="<article>{{Front}}</article>",
                    afmt="{{FrontSide}}<hr id=answer>{{Back}}{{#Extra}}<aside>{{Extra}}</aside>{{/Extra}}",
                )
            ],
            css=".card { color: coral; }",
            reuse_existing=True,
        ),
        notes=[NoteSpec(fields={"Front": "Q", "Back": "A", "Extra": "More"}, tags=[])],
    )

    summary = import_bundle(
        collection=collection,
        bundle=bundle,
        selected_notetype_id=7,
        selected_deck_id=100,
        request_factory=FakeAddNoteRequest,
    )

    updated = collection.models.by_name("Beautiful Basic")
    assert updated is not None
    assert summary.created_note_type is False
    assert summary.updated_note_type is True
    assert collection.models.updated_ids == [7]
    assert collection.models.field_names(updated) == ["Front", "Back", "Extra"]
    assert updated["css"] == ".card { color: coral; }"


def test_import_bundle_rejects_unknown_fields_for_selected_note_type() -> None:
    collection = FakeCollection(
        [
            {
                "id": 42,
                "name": "Basic",
                "flds": [{"name": "Front"}, {"name": "Back"}],
                "tmpls": [{"name": "Card 1", "qfmt": "{{Front}}", "afmt": "{{Back}}"}],
                "css": "",
            }
        ]
    )
    bundle = CardBundle(
        version=1,
        note_type=None,
        notes=[NoteSpec(fields={"Front": "Q", "Back": "A", "Extra": "Nope"}, tags=[])],
    )

    with pytest.raises(
        BundleValidationError,
        match="Note 1 uses unknown fields for note type 'Basic': Extra",
    ):
        import_bundle(
            collection=collection,
            bundle=bundle,
            selected_notetype_id=42,
            selected_deck_id=100,
            request_factory=FakeAddNoteRequest,
        )
