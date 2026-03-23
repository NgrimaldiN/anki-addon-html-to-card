from __future__ import annotations

import pytest

from addon.errors import BundleValidationError
from addon.parser import parse_bundle_text


def test_parse_bundle_text_accepts_raw_json() -> None:
    bundle = parse_bundle_text(
        """
        {
          "version": 1,
          "notes": [
            {
              "fields": {
                "Front": "<h1>Question</h1>",
                "Back": "<p>Answer</p>"
              }
            }
          ]
        }
        """
    )

    assert bundle["version"] == 1
    assert bundle["notes"][0]["fields"]["Front"] == "<h1>Question</h1>"


def test_parse_bundle_text_accepts_fenced_json_block() -> None:
    bundle = parse_bundle_text(
        """
        Here is your bundle:

        ```json
        {
          "version": 1,
          "notes": [
            {
              "fields": {
                "Front": "Q",
                "Back": "A"
              },
              "tags": ["llm", "generated"]
            }
          ]
        }
        ```
        """
    )

    assert bundle["notes"][0]["fields"]["Back"] == "A"
    assert bundle["notes"][0]["tags"] == ["llm", "generated"]


def test_parse_bundle_text_accepts_json_with_line_comments() -> None:
    bundle = parse_bundle_text(
        """
        {
          // Keep the currently selected Anki note type by default.
          "version": 1,
          "notes": [
            {
              "fields": {
                "Front": "Q",
                "Back": "First line\\nSecond line",
                "Extra": "More"
              }
            }
          ]
        }
        """
    )

    assert bundle["notes"][0]["fields"]["Back"] == "First line\nSecond line"


def test_parse_bundle_text_accepts_json_with_block_comments() -> None:
    bundle = parse_bundle_text(
        """
        ```json
        {
          /* Include note_type only when you really need custom
             fields, templates, or CSS. */
          "version": 1,
          "notes": [
            {
              "fields": {
                "Front": "Q",
                "Back": "A"
              }
            }
          ]
        }
        ```
        """
    )

    assert bundle["version"] == 1


def test_parse_bundle_text_preserves_comment_markers_inside_strings() -> None:
    bundle = parse_bundle_text(
        """
        {
          // This comment should be stripped.
          "version": 1,
          "notes": [
            {
              "fields": {
                "Front": "Visit https://example.com/docs",
                "Back": "Literal /* keep me */ text"
              }
            }
          ]
        }
        """
    )

    assert bundle["notes"][0]["fields"]["Front"] == "Visit https://example.com/docs"
    assert bundle["notes"][0]["fields"]["Back"] == "Literal /* keep me */ text"


def test_parse_bundle_text_rejects_invalid_json_with_helpful_message() -> None:
    with pytest.raises(BundleValidationError, match="valid JSON object"):
        parse_bundle_text(
            """
            ```json
            {
              "notes": [
            ```
            """
        )
