"""Pure helpers for matching app and window names."""

from __future__ import annotations

from typing import Any


def duplicates_removed(items: list[Any]) -> list[Any]:
    """Return items in original order with duplicates removed."""
    seen: set[Any] = set()
    return [item for item in items if item not in seen and not seen.add(item)]


def hierarchical_name_match(
    target_name: str,
    candidates: list[tuple[str, Any]],
    match_start: bool,
    match_anywhere: bool,
    match_fuzzy: bool,
) -> list[Any]:
    """Return candidates ranked by increasingly fuzzy name matching."""
    target_name = target_name.lower()
    lowered_candidates = [(key.lower(), value) for (key, value) in candidates]
    results: list[Any] = []

    for name, value in lowered_candidates:
        if name == target_name:
            results.append(value)

    if match_start:
        for name, value in lowered_candidates:
            if name.startswith(target_name):
                results.append(value)

    if match_anywhere:
        for name, value in lowered_candidates:
            if target_name in name:
                results.append(value)

    if match_fuzzy:
        target_words = target_name.split(" ")
        for name, value in lowered_candidates:
            if all(word in name.split(" ") for word in target_words):
                results.append(value)

    return duplicates_removed(results)


def heirarchical_name_match(
    target_name: str,
    candidates: list[tuple[str, Any]],
    match_start: bool,
    match_anywhere: bool,
    match_fuzzy: bool,
) -> list[Any]:
    """Compatibility shim for the historical misspelling used by actions/tests."""
    return hierarchical_name_match(
        target_name,
        candidates,
        match_start,
        match_anywhere,
        match_fuzzy,
    )
