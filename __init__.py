from __future__ import annotations

import sys
from pathlib import Path


_ADDON_ROOT = str(Path(__file__).resolve().parent)
if _ADDON_ROOT not in sys.path:
    sys.path.insert(0, _ADDON_ROOT)

try:
    import aqt  # noqa: F401
except ImportError:
    pass
else:
    from addon.entry import register_addon

    register_addon()
