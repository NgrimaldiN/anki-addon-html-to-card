from __future__ import annotations

try:
    import aqt  # noqa: F401
except ImportError:
    pass
else:
    from addon.entry import register_addon

    register_addon()
