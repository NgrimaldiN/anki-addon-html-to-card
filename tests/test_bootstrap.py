from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


def test_addon_bootstrap_loads_local_package_without_preexisting_sys_path(
    monkeypatch,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    original_sys_path = list(sys.path)
    filtered_sys_path = [
        entry
        for entry in original_sys_path
        if not _same_path(entry, repo_root)
    ]
    monkeypatch.setattr(sys, "path", filtered_sys_path)

    for module_name in list(sys.modules):
        if module_name == "addon" or module_name.startswith("addon."):
            sys.modules.pop(module_name, None)

    fake_modules = _install_fake_aqt_modules()
    monkeypatch.setattr(sys, "modules", {**sys.modules, **fake_modules})

    spec = importlib.util.spec_from_file_location(
        "paste_llm_cards_loader_test",
        repo_root / "__init__.py",
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert str(repo_root) == sys.path[0]


def _same_path(entry: str, target: Path) -> bool:
    if not entry:
        return False
    try:
        return Path(entry).resolve() == target.resolve()
    except OSError:
        return False


def _install_fake_aqt_modules() -> dict[str, types.ModuleType]:
    fake_aqt = types.ModuleType("aqt")
    fake_aqt.__path__ = []  # type: ignore[attr-defined]

    fake_gui_hooks = types.ModuleType("aqt.gui_hooks")
    fake_gui_hooks.add_cards_did_init = _HookList()

    fake_qt = types.ModuleType("aqt.qt")

    class _ButtonRole:
        ActionRole = object()

    class QDialogButtonBox:
        ButtonRole = _ButtonRole

    class _Clipboard:
        def setText(self, _text: str) -> None:
            pass

    class QApplication:
        @staticmethod
        def clipboard() -> _Clipboard:
            return _Clipboard()

    class QPushButton:
        def __init__(self, *args, **kwargs) -> None:
            self.clicked = _Signal()

        def setToolTip(self, _text: str) -> None:
            pass

    class QDialog:
        pass

    class QHBoxLayout:
        pass

    class QLabel:
        def __init__(self, *args, **kwargs) -> None:
            pass

    class QPlainTextEdit:
        def __init__(self, *args, **kwargs) -> None:
            self.textChanged = _Signal()

    class QVBoxLayout:
        pass

    fake_qt.QApplication = QApplication
    fake_qt.QDialogButtonBox = QDialogButtonBox
    fake_qt.QPushButton = QPushButton
    fake_qt.QDialog = QDialog
    fake_qt.QHBoxLayout = QHBoxLayout
    fake_qt.QLabel = QLabel
    fake_qt.QPlainTextEdit = QPlainTextEdit
    fake_qt.QVBoxLayout = QVBoxLayout

    fake_operations = types.ModuleType("aqt.operations")

    class CollectionOp:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def success(self, _callback):
            return self

        def failure(self, _callback):
            return self

        def run_in_background(self, *, initiator=None) -> None:
            return None

    fake_operations.CollectionOp = CollectionOp

    fake_utils = types.ModuleType("aqt.utils")
    fake_utils.showWarning = lambda *args, **kwargs: None
    fake_utils.tooltip = lambda *args, **kwargs: None

    fake_aqt.gui_hooks = fake_gui_hooks

    return {
        "aqt": fake_aqt,
        "aqt.gui_hooks": fake_gui_hooks,
        "aqt.qt": fake_qt,
        "aqt.operations": fake_operations,
        "aqt.utils": fake_utils,
    }


class _HookList(list):
    pass


class _Signal:
    def connect(self, _callback) -> None:
        pass
