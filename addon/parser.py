from __future__ import annotations

import json
import re
from typing import Any

from addon.errors import BundleValidationError


_FENCED_JSON_RE = re.compile(r"```jsonc?\s*(?P<body>.*?)```", re.IGNORECASE | re.DOTALL)


def parse_bundle_text(text: str) -> dict[str, Any]:
    candidate = _extract_json_candidate(text)
    if not candidate:
        raise BundleValidationError("Paste a valid JSON object before importing.")
    candidate = _strip_json_comments(candidate)
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise BundleValidationError(
            f"The pasted content must be a valid JSON object. {exc.msg} at line "
            f"{exc.lineno}, column {exc.colno}."
        ) from exc
    if not isinstance(parsed, dict):
        raise BundleValidationError("The pasted content must decode to a JSON object.")
    return parsed


def _extract_json_candidate(text: str) -> str:
    match = _FENCED_JSON_RE.search(text)
    if match:
        return match.group("body").strip()
    return text.strip()


def _strip_json_comments(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    in_line_comment = False
    in_block_comment = False
    index = 0

    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
                result.append(char)
            index += 1
            continue

        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                index += 2
            else:
                if char == "\n":
                    result.append(char)
                index += 1
            continue

        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue

        if char == "/" and next_char == "/":
            in_line_comment = True
            index += 2
            continue

        if char == "/" and next_char == "*":
            in_block_comment = True
            index += 2
            continue

        result.append(char)
        index += 1

    return "".join(result)
