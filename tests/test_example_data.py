from __future__ import annotations

from addon.example_data import (
    CUSTOM_NOTE_TYPE_EXAMPLE_TEXT,
    EXAMPLE_BUNDLE_TEXT,
    LLM_GENERATION_GUIDANCE,
    LLM_PROMPT_TEXT,
)
from addon.service import bundle_from_text


def test_example_bundle_defaults_to_native_anki_basic_structure() -> None:
    bundle = bundle_from_text(EXAMPLE_BUNDLE_TEXT)

    assert bundle.note_type is None
    assert bundle.notes[0].fields["Front"] == "Write the question, term, or prompt here."
    assert (
        bundle.notes[0].fields["Back"]
        == "Write the answer or explanation here. Use \\n for intentional line breaks inside the string."
    )
    assert set(bundle.notes[0].fields) == {"Front", "Back"}
    assert "CRITICAL JSON FORMATTING RULE" in EXAMPLE_BUNDLE_TEXT
    assert "//" in EXAMPLE_BUNDLE_TEXT


def test_custom_note_type_example_defines_extra_and_templates_explicitly() -> None:
    bundle = bundle_from_text(CUSTOM_NOTE_TYPE_EXAMPLE_TEXT)

    assert bundle.note_type is not None
    assert bundle.note_type.fields == ["Front", "Back", "Extra"]
    assert bundle.notes[0].fields["Extra"] == "Optional detail, nuance, mnemonic, or example."


def test_llm_generation_guidance_prefers_native_output_but_allows_creativity() -> None:
    assert "native-looking Anki Basic card" in LLM_GENERATION_GUIDANCE
    assert "fully custom HTML/CSS" in LLM_GENERATION_GUIDANCE
    assert "unless the user explicitly asks" in LLM_GENERATION_GUIDANCE
    assert "omit note_type" in LLM_GENERATION_GUIDANCE
    assert "If you use Extra" in LLM_GENERATION_GUIDANCE
    assert "include a complete note_type block" in LLM_GENERATION_GUIDANCE
    assert "\\n" in LLM_GENERATION_GUIDANCE
    assert "Return only one fenced json block or one raw JSON object" in LLM_GENERATION_GUIDANCE
    assert "select Anki's working 'Basic' note type first" in LLM_GENERATION_GUIDANCE
    assert "\\\\(" in LLM_GENERATION_GUIDANCE
    assert "\\\\[" in LLM_GENERATION_GUIDANCE
    assert "\\\\mathbb{E}" in LLM_GENERATION_GUIDANCE
    assert "\\\\mathbb{P}" in LLM_GENERATION_GUIDANCE
    assert "Do not use \\n to make math render" in LLM_GENERATION_GUIDANCE
    assert "Return only one JSON object" in LLM_GENERATION_GUIDANCE
    assert "no trailing semicolon" in LLM_GENERATION_GUIDANCE


def test_example_bundle_text_warns_about_json_wrapping_and_math_escaping() -> None:
    assert "RETURN ONLY THIS JSON OBJECT" in EXAMPLE_BUNDLE_TEXT
    assert 'working note type like "Basic"' in EXAMPLE_BUNDLE_TEXT
    assert 'If you want "Extra"' in EXAMPLE_BUNDLE_TEXT
    assert "\\\\mathbb{E}" in EXAMPLE_BUNDLE_TEXT
    assert "\\\\(" in EXAMPLE_BUNDLE_TEXT


def test_llm_prompt_text_is_a_copyable_strict_output_prompt() -> None:
    assert "Return only one fenced ```json``` block." in LLM_PROMPT_TEXT
    assert 'If you omit "note_type"' in LLM_PROMPT_TEXT
    assert 'If you use "Extra", any field beyond "Front"/"Back"' in LLM_PROMPT_TEXT
    assert "\\\\(" in LLM_PROMPT_TEXT
    assert "\\\\[" in LLM_PROMPT_TEXT
    assert "\\\\mathbb{E}" in LLM_PROMPT_TEXT
    assert "\\\\mathbb{P}" in LLM_PROMPT_TEXT
    assert "Do not use \\n to make math render" in LLM_PROMPT_TEXT
    assert "Safe default example:" in LLM_PROMPT_TEXT
    assert "Custom note_type example:" in LLM_PROMPT_TEXT
    assert EXAMPLE_BUNDLE_TEXT in LLM_PROMPT_TEXT
    assert CUSTOM_NOTE_TYPE_EXAMPLE_TEXT in LLM_PROMPT_TEXT
