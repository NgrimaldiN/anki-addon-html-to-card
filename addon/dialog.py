from __future__ import annotations

from typing import Any

from aqt.operations import CollectionOp
from aqt.qt import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)
from aqt.utils import showWarning, tooltip

from addon.errors import BundleError
from addon.example_data import EXAMPLE_BUNDLE_TEXT, LLM_PROMPT_TEXT
from addon.importer import (
    ImportSummary,
    assess_note_type_health,
    find_working_basic_note_type,
    import_bundle,
)
from addon.service import bundle_from_text, summarize_bundle


class PasteCardsDialog(QDialog):
    def __init__(self, addcards: Any) -> None:
        super().__init__(addcards)
        self._addcards = addcards
        self._bundle = None
        self._warning_details = ""
        self.setWindowTitle("Paste LLM Cards")
        self.resize(780, 620)
        self._setup_ui()
        self._refresh_context_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        intro = QLabel(
            "Paste one JSON bundle to add notes directly into the current deck."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        context_row = QHBoxLayout()
        context_row.setSpacing(10)
        layout.addLayout(context_row)

        self.deck_label = QLabel(self)
        context_row.addWidget(self.deck_label)

        self.note_type_label = QLabel(self)
        context_row.addWidget(self.note_type_label)

        context_row.addStretch(1)

        self.health_badge = QLabel(self)
        self.health_badge.setStyleSheet("")
        context_row.addWidget(self.health_badge)

        steps_label = QLabel("1. Copy LLM Prompt   2. Generate strict JSON   3. Paste and import")
        steps_label.setWordWrap(True)
        layout.addWidget(steps_label)

        warning_row = QHBoxLayout()
        warning_row.setSpacing(8)
        layout.addLayout(warning_row)

        self.warning_label = QLabel(self)
        self.warning_label.setWordWrap(True)
        warning_row.addWidget(self.warning_label, 1)

        self.switch_basic_button = QPushButton("Switch to Basic", self)
        self.switch_basic_button.clicked.connect(self._switch_to_basic)
        warning_row.addWidget(self.switch_basic_button)

        self.warning_help_button = QPushButton("Why this warning?", self)
        self.warning_help_button.clicked.connect(self._show_warning_details)
        warning_row.addWidget(self.warning_help_button)

        self.bundle_input = QPlainTextEdit(self)
        self.bundle_input.setPlaceholderText(
            "Paste the JSON bundle here.\n\nUse Copy LLM Prompt if you want a strict prompt\n"
            "for another model, or Copy Format Example if you want the raw schema."
        )
        self.bundle_input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.bundle_input, 1)

        self.prompt_preview = QPlainTextEdit(self)
        self.prompt_preview.setReadOnly(True)
        self.prompt_preview.setPlainText(LLM_PROMPT_TEXT)
        self.prompt_preview.hide()
        layout.addWidget(self.prompt_preview)

        self.status_label = QLabel("Paste a bundle, then import it.")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        layout.addLayout(buttons)

        self.prompt_button = QPushButton("Copy LLM Prompt", self)
        self.prompt_button.clicked.connect(self._copy_llm_prompt)
        buttons.addWidget(self.prompt_button)

        self.preview_prompt_button = QPushButton("Preview Prompt", self)
        self.preview_prompt_button.clicked.connect(self._toggle_prompt_preview)
        buttons.addWidget(self.preview_prompt_button)

        self.example_button = QPushButton("Copy Format Example", self)
        self.example_button.clicked.connect(self._copy_example)
        buttons.addWidget(self.example_button)

        buttons.addStretch(1)

        self.import_button = QPushButton("Import Cards", self)
        self.import_button.setDefault(True)
        self.import_button.clicked.connect(self._import_cards)
        buttons.addWidget(self.import_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        buttons.addWidget(self.cancel_button)

    def _on_text_changed(self) -> None:
        self._bundle = None
        self.status_label.setText("Bundle changed. Import to validate and continue.")

    def _copy_example(self) -> None:
        QApplication.clipboard().setText(EXAMPLE_BUNDLE_TEXT)
        tooltip("Format example copied to clipboard.", period=2500)
        self.status_label.setText(
            "Format example copied to clipboard. Paste it into another LLM or edit it here."
        )

    def _copy_llm_prompt(self) -> None:
        QApplication.clipboard().setText(LLM_PROMPT_TEXT)
        tooltip("LLM prompt copied to clipboard.", period=2500)
        self.status_label.setText(
            "Strict LLM prompt copied to clipboard. Generate one JSON block, then paste it here."
        )

    def _toggle_prompt_preview(self) -> None:
        is_visible = self.prompt_preview.isVisible()
        self.prompt_preview.setVisible(not is_visible)
        self.preview_prompt_button.setText("Hide Prompt" if not is_visible else "Preview Prompt")

    def _parse_current_bundle(self):
        try:
            bundle = bundle_from_text(self.bundle_input.toPlainText())
        except BundleError as exc:
            showWarning(str(exc), parent=self)
            self.status_label.setText("Validation failed. Fix the bundle and try again.")
            return None

        self._bundle = bundle
        self.status_label.setText(summarize_bundle(bundle))
        return bundle

    def _import_cards(self) -> None:
        bundle = self._bundle or self._parse_current_bundle()
        if bundle is None:
            return

        from anki.collection import AddNoteRequest

        selected_deck_id = self._addcards.deck_chooser.selected_deck_id
        selected_notetype_id = self._addcards.notetype_chooser.selected_notetype_id

        self._set_busy(True)

        CollectionOp(
            self,
            lambda col: import_bundle(
                collection=col,
                bundle=bundle,
                selected_notetype_id=selected_notetype_id,
                selected_deck_id=selected_deck_id,
                request_factory=AddNoteRequest,
            ),
        ).success(self._on_import_success).failure(self._on_import_failure).run_in_background(
            initiator=self
        )

    def _on_import_success(self, summary: ImportSummary) -> None:
        self._set_busy(False)
        self.status_label.setText(self._success_message(summary))
        tooltip(self._success_message(summary), period=4000)
        self.accept()

    def _on_import_failure(self, error: Exception) -> None:
        self._set_busy(False)
        self._refresh_context_ui()
        showWarning(str(error), parent=self)
        self.status_label.setText("Import failed. Review the error and try again.")

    def _set_busy(self, is_busy: bool) -> None:
        self.bundle_input.setEnabled(not is_busy)
        self.prompt_button.setEnabled(not is_busy)
        self.preview_prompt_button.setEnabled(not is_busy)
        self.example_button.setEnabled(not is_busy)
        self.import_button.setEnabled(not is_busy)
        self.cancel_button.setEnabled(not is_busy)
        self.switch_basic_button.setEnabled(not is_busy)
        self.warning_help_button.setEnabled(not is_busy)

    def _success_message(self, summary: ImportSummary) -> str:
        note_word = "note" if summary.note_count == 1 else "notes"
        message = f"Added {summary.note_count} {note_word} from the pasted bundle."
        if summary.created_note_type:
            return (
                f"{message} Created note type '{summary.note_type_name}'. "
                "Anki may request a full sync because the note type changed."
            )
        if summary.updated_note_type:
            return (
                f"{message} Updated note type '{summary.note_type_name}'. "
                "Anki may request a full sync because the note type changed."
            )
        return message

    def _refresh_context_ui(self) -> None:
        collection = self._collection()
        deck_id = self._addcards.deck_chooser.selected_deck_id
        note_type_id = self._addcards.notetype_chooser.selected_notetype_id
        note_type = collection.models.get(note_type_id)
        health = assess_note_type_health(collection.models, note_type)

        self.deck_label.setText(f"Deck: {self._deck_name(collection, deck_id)}")
        self.note_type_label.setText(
            f"Note type: {note_type['name'] if note_type is not None else str(note_type_id)}"
        )

        if health.is_ready:
            self.health_badge.setText("Ready")
            self.health_badge.setStyleSheet(
                "QLabel { background: #dff3e4; color: #136c2e; border-radius: 10px; "
                "padding: 3px 10px; font-weight: 600; }"
            )
            self.warning_label.hide()
            self.switch_basic_button.hide()
            self.warning_help_button.hide()
            self._warning_details = ""
            return

        self.health_badge.setText("Needs attention")
        self.health_badge.setStyleSheet(
            "QLabel { background: #fff0d9; color: #8a4b00; border-radius: 10px; "
            "padding: 3px 10px; font-weight: 600; }"
        )
        broken_templates = ", ".join(health.broken_templates)
        self.warning_label.setText(
            "Current note type has a broken back template. Imports that omit note_type will fail."
        )
        self._warning_details = (
            f"Selected note type '{note_type['name'] if note_type is not None else note_type_id}' "
            f"has template(s) without any real field reference: {broken_templates}. "
            "Switch Add Cards to a working note type like 'Basic', or import a bundle "
            "that includes a complete note_type block."
        )
        self.warning_label.show()
        self.warning_help_button.show()
        self.switch_basic_button.setVisible(find_working_basic_note_type(collection.models) is not None)

    def _show_warning_details(self) -> None:
        if self._warning_details:
            showWarning(self._warning_details, parent=self)

    def _switch_to_basic(self) -> None:
        collection = self._collection()
        basic = find_working_basic_note_type(collection.models)
        if basic is None:
            showWarning(
                "A working note type named 'Basic' was not found. Please switch Add Cards "
                "to a healthy note type manually.",
                parent=self,
            )
            return

        if hasattr(self._addcards, "set_note_type"):
            self._addcards.set_note_type(basic["id"])
        else:
            self._addcards.notetype_chooser.selected_notetype_id = basic["id"]

        self._refresh_context_ui()
        tooltip("Switched Add Cards to Basic.", period=2500)
        self.status_label.setText(
            "Switched Add Cards to Basic. Imports that omit note_type will now target Basic."
        )

    def _collection(self) -> Any:
        if hasattr(self._addcards, "col"):
            return self._addcards.col
        return self._addcards.mw.col

    def _deck_name(self, collection: Any, deck_id: Any) -> str:
        decks = collection.decks
        if hasattr(decks, "name"):
            try:
                name = decks.name(deck_id)
                if name:
                    return str(name)
            except Exception:
                pass

        if hasattr(decks, "get"):
            try:
                deck = decks.get(deck_id)
            except Exception:
                deck = None
            if isinstance(deck, dict) and deck.get("name"):
                return str(deck["name"])

        return str(deck_id)
