from __future__ import annotations

from addon.example_data import EXAMPLE_BUNDLE_TEXT, LLM_GENERATION_GUIDANCE
from addon.service import bundle_from_text


def test_example_bundle_defaults_to_native_anki_basic_structure() -> None:
    bundle = bundle_from_text(EXAMPLE_BUNDLE_TEXT)

    assert bundle.note_type is not None
    assert bundle.note_type.name == "LLM Basic"
    assert bundle.note_type.fields == ["Front", "Back", "Extra"]
    assert bundle.note_type.templates[0].qfmt == "{{Front}}"
    assert "{{FrontSide}}" in bundle.note_type.templates[0].afmt
    assert "<hr id=answer>" in bundle.note_type.templates[0].afmt
    assert "Prompt" not in bundle.note_type.templates[0].qfmt
    assert "text-align: center;" in bundle.note_type.css
    assert "font-family: arial;" in bundle.note_type.css


def test_llm_generation_guidance_prefers_native_output_but_allows_creativity() -> None:
    assert "native-looking Anki Basic card" in LLM_GENERATION_GUIDANCE
    assert "fully custom HTML/CSS" in LLM_GENERATION_GUIDANCE
    assert "unless the user explicitly asks" in LLM_GENERATION_GUIDANCE
