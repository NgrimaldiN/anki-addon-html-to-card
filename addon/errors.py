from __future__ import annotations


class BundleError(Exception):
    """Base exception for bundle parsing and import failures."""


class BundleValidationError(BundleError):
    """Raised when the pasted bundle has an invalid structure."""
