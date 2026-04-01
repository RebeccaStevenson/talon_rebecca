"""Pure source-resolution helpers for preview sync."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlparse


def candidate_relative_paths(url: str) -> list[Path]:
    """Return plausible source-relative paths for a preview URL."""
    parsed = urlparse(url)
    raw_path = unquote(parsed.path or "/")
    rel = raw_path.lstrip("/")

    if not rel:
        rel = "index.html"

    if rel.endswith("/"):
        rel += "index.html"

    variants = [rel]
    if rel.startswith("_site/"):
        variants.append(rel[len("_site/") :])

    output = []
    for item in variants:
        path = Path(item)
        if path.suffix.lower() == ".html":
            output.append(path.with_suffix(".qmd"))
            output.append(path.with_suffix(".md"))
        else:
            output.append(path)
    return output


def resolve_source_path(url: str, roots: list[Path], cache: dict[str, Path]) -> Path | None:
    """Resolve a source path from a preview URL using configured roots."""
    cached = cache.get(url)
    if cached and cached.exists():
        return cached

    rel_candidates = candidate_relative_paths(url)
    for root in roots:
        root_resolved = root.resolve()
        for rel in rel_candidates:
            candidate = (root / rel).resolve()
            try:
                candidate.relative_to(root_resolved)
            except ValueError:
                continue
            if candidate.exists() and candidate.is_file():
                cache[url] = candidate
                return candidate

    parsed = urlparse(url)
    url_parts = [part for part in unquote(parsed.path).split("/") if part]
    best_match: Path | None = None
    best_score = -1

    for rel in rel_candidates:
        basename = rel.name
        if not basename:
            continue
        rel_parts = rel.parts

        for root in roots:
            try:
                candidates = root.rglob(basename)
            except Exception:
                continue

            for candidate in candidates:
                if not candidate.is_file():
                    continue

                cand_parts = candidate.parts
                tail_score = 0
                max_tail = min(len(rel_parts), len(cand_parts))
                for index in range(1, max_tail + 1):
                    if cand_parts[-index] == rel_parts[-index]:
                        tail_score += 1
                    else:
                        break

                url_tail = 0
                max_url_tail = min(len(url_parts), len(cand_parts))
                for index in range(1, max_url_tail + 1):
                    if cand_parts[-index] == url_parts[-index]:
                        url_tail += 1
                    else:
                        break

                score = (tail_score * 10) + url_tail
                if score > best_score:
                    best_score = score
                    best_match = candidate

    if best_match:
        cache[url] = best_match
        return best_match

    return None


def normalize_stem(value: str) -> str:
    """Normalize a source hint or filename stem for matching."""
    return (
        value.strip()
        .lower()
        .replace(".md", "")
        .replace(".qmd", "")
        .replace(".html", "")
    )


def resolve_by_hints(source_hints: list[str] | None, roots: list[Path]) -> Path | None:
    """Resolve a source path from title/name hints."""
    if not source_hints:
        return None

    normalized_hints = [normalize_stem(hint) for hint in source_hints if hint and hint.strip()]
    normalized_hints = [hint for hint in normalized_hints if hint]
    if not normalized_hints:
        return None

    best_match: Path | None = None
    best_score = -1

    for root in roots:
        try:
            files = root.rglob("*")
        except Exception:
            continue

        for candidate in files:
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in (".md", ".qmd"):
                continue

            stem_norm = candidate.stem.lower()
            for hint in normalized_hints:
                score = 0
                if stem_norm == hint:
                    score = 100
                elif stem_norm.endswith(hint) or hint.endswith(stem_norm):
                    score = 80
                elif hint in stem_norm:
                    score = 60

                if score > best_score:
                    best_score = score
                    best_match = candidate

    return best_match


def is_allowed_origin(origin: str | None) -> bool:
    """Allow only localhost browser origins."""
    if not origin:
        return True
    try:
        parsed = urlparse(origin)
    except Exception:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.hostname or "").lower()
    return host in {"localhost", "127.0.0.1"}


def sanitize_source_hints(
    raw_hints, *, max_hints: int, max_hint_chars: int
) -> list[str]:
    """Trim and bound user-provided source hints."""
    if not isinstance(raw_hints, list):
        return []

    output = []
    for item in raw_hints[:max_hints]:
        if not isinstance(item, str):
            continue
        value = item.strip()
        if not value:
            continue
        output.append(value[:max_hint_chars])
    return output


def scope_from_url(url: str) -> str:
    """Return scheme+host(+port) scope for a page URL."""
    try:
        parsed = urlparse(url)
    except Exception:
        return ""
    if not parsed.scheme or not parsed.netloc:
        return ""
    return f"{parsed.scheme}://{parsed.netloc}".lower()


def sanitize_scope(raw_scope: str | None, page_url: str) -> str:
    """Normalize an explicit or derived preview scope."""
    scope = (raw_scope or "").strip().lower()
    if scope:
        parsed = urlparse(scope)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}".lower()
    return scope_from_url(page_url)
