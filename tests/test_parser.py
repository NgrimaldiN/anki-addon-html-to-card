from __future__ import annotations

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
