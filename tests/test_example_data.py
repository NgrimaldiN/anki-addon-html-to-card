from __future__ import annotations

from addon.example_data import EXAMPLE_BUNDLE_TEXT, LLM_GENERATION_GUIDANCE
from addon.service import bundle_from_text


def test_example_bundle_defaults_to_native_anki_basic_structure() -> None:
    bundle = bundle_from_text(EXAMPLE_BUNDLE_TEXT)

    assert bundle.note_type is None
    assert bundle.notes[0].fields["Front"] == "Write the question, term, or prompt here."
    assert bundle.notes[0].fields["Back"] == "Write the answer or explanation here."
    assert bundle.notes[0].fields["Extra"] == "Optional detail, nuance, mnemonic, or example."


def test_llm_generation_guidance_prefers_native_output_but_allows_creativity() -> None:
    assert "native-looking Anki Basic card" in LLM_GENERATION_GUIDANCE
    assert "fully custom HTML/CSS" in LLM_GENERATION_GUIDANCE
    assert "unless the user explicitly asks" in LLM_GENERATION_GUIDANCE
    assert "omit note_type" in LLM_GENERATION_GUIDANCE
