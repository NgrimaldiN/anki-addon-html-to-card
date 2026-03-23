from __future__ import annotations

from typing import Any

from aqt import gui_hooks
from aqt.qt import QDialogButtonBox, QPushButton

from addon.dialog import PasteCardsDialog


_REGISTERED = False
_BUTTON_ATTR = "_paste_llm_cards_button"


def register_addon() -> None:
    global _REGISTERED

    if _REGISTERED:
        return
    gui_hooks.add_cards_did_init.append(_on_add_cards_did_init)
    _REGISTERED = True


def _on_add_cards_did_init(addcards: Any) -> None:
    if getattr(addcards, _BUTTON_ATTR, None) is not None:
        return

    button = QPushButton("Paste LLM Cards", addcards)
    button.setToolTip(
        "Paste an LLM JSON bundle and add one or many notes directly to the selected deck."
    )
    button.clicked.connect(lambda: _open_dialog(addcards))
    addcards.form.buttonBox.addButton(button, QDialogButtonBox.ButtonRole.ActionRole)
    setattr(addcards, _BUTTON_ATTR, button)


def _open_dialog(addcards: Any) -> None:
    dialog = PasteCardsDialog(addcards)
    dialog.exec()
