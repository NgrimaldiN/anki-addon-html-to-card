from __future__ import annotations

import json
import re
from typing import Any

from addon.errors import BundleValidationError


_FENCED_JSON_RE = re.compile(r"```json\s*(?P<body>.*?)```", re.IGNORECASE | re.DOTALL)


def parse_bundle_text(text: str) -> dict[str, Any]:
    candidate = _extract_json_candidate(text)
    if not candidate:
        raise BundleValidationError("Paste a valid JSON object before importing.")
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
