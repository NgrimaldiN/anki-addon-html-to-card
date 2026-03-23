from __future__ import annotations

from addon.service import bundle_from_text, summarize_bundle


def test_bundle_from_text_parses_and_normalizes_fenced_json() -> None:
    bundle = bundle_from_text(
        """
        ```json
        {
          "version": 1,
          "notes": [
            {
              "fields": {
                "Front": "Question",
                "Back": "Answer"
              }
            }
          ]
        }
        ```
        """
    )

    assert bundle.version == 1
    assert bundle.note_type is None
    assert bundle.notes[0].fields["Back"] == "Answer"
    assert bundle.notes[0].tags == []


def test_summarize_bundle_describes_custom_note_type_and_note_count() -> None:
    bundle = bundle_from_text(
        """
        {
          "version": 1,
          "note_type": {
            "name": "Beautiful Basic",
            "fields": ["Front", "Back"],
            "templates": [
              {
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Back}}"
              }
            ],
            "css": ".card { color: teal; }"
          },
          "notes": [
            {
              "fields": {
                "Front": "Q1",
                "Back": "A1"
              }
            },
            {
              "fields": {
                "Front": "Q2",
                "Back": "A2"
              }
            }
          ]
        }
        """
    )

    assert (
        summarize_bundle(bundle)
        == "2 notes targeting custom note type 'Beautiful Basic'."
    )
