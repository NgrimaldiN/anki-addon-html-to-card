from __future__ import annotations

import json
import re
from typing import Any


_FENCED_JSON_RE = re.compile(r"```json\s*(?P<body>.*?)```", re.IGNORECASE | re.DOTALL)


def parse_bundle_text(text: str) -> dict[str, Any]:
    candidate = _extract_json_candidate(text)
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise ValueError("The pasted bundle must decode to a JSON object.")
    return parsed


def _extract_json_candidate(text: str) -> str:
    match = _FENCED_JSON_RE.search(text)
    if match:
        return match.group("body").strip()
    return text.strip()
