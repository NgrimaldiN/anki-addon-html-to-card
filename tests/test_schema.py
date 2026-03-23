from __future__ import annotations

import pytest

from addon.errors import BundleValidationError
from addon.schema import normalize_bundle


def test_normalize_bundle_accepts_minimal_notes_payload() -> None:
    bundle = normalize_bundle(
        {
            "version": 1,
            "notes": [
                {
                    "fields": {
                        "Front": "<h1>Hello</h1>",
                        "Back": "<p>World</p>",
                    }
                }
            ],
        }
    )

    assert bundle.version == 1
    assert bundle.note_type is None
    assert bundle.notes[0].fields["Front"] == "<h1>Hello</h1>"
    assert bundle.notes[0].tags == []


def test_normalize_bundle_rejects_unknown_top_level_key() -> None:
    with pytest.raises(BundleValidationError, match="Unknown top-level key: deck"):
        normalize_bundle(
            {
                "version": 1,
                "deck": "Default",
                "notes": [{"fields": {"Front": "Q", "Back": "A"}}],
            }
        )


def test_normalize_bundle_rejects_note_field_missing_from_custom_note_type() -> None:
    with pytest.raises(
        BundleValidationError,
        match="Note 1 uses unknown fields for note type 'Beautiful Basic': Extra",
    ):
        normalize_bundle(
            {
                "version": 1,
                "note_type": {
                    "name": "Beautiful Basic",
                    "fields": ["Front", "Back"],
                    "templates": [
                        {
                            "name": "Card 1",
                            "qfmt": "{{Front}}",
                            "afmt": "{{FrontSide}}<hr id=answer>{{Back}}",
                        }
                    ],
                    "css": ".card { color: black; }",
                },
                "notes": [
                    {"fields": {"Front": "Q", "Back": "A", "Extra": "Oops"}},
                ],
            }
        )


def test_normalize_bundle_rejects_back_template_without_declared_field_references() -> None:
    with pytest.raises(
        BundleValidationError,
        match="Template 'Card 1' back format must reference at least one declared field",
    ):
        normalize_bundle(
            {
                "version": 1,
                "note_type": {
                    "name": "Broken Basic",
                    "fields": ["Front", "Back", "Extra"],
                    "templates": [
                        {
                            "name": "Card 1",
                            "qfmt": "{{Front}}",
                            "afmt": '{{FrontSide}}<br><br><hr id="answer"><br><br><br><br><div class="extra"></div>',
                        }
                    ],
                    "css": ".card { color: black; }",
                },
                "notes": [
                    {"fields": {"Front": "Q", "Back": "A", "Extra": "More"}},
                ],
            }
        )
