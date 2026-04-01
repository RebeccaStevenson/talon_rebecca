"""Tests for tools/preview_sync/capture_server.py path resolution and capture behavior."""

import sys

if "pytest" in sys.modules:
    from pathlib import Path

    import user.talon_rebecca.tools.preview_sync.capture_server as mod

    def _set_roots(monkeypatch, tmp_path: Path):
        roots_file = tmp_path / "preview_sync_roots.json"
        roots_file.write_text(f'{{"roots": ["{tmp_path}"]}}\n', encoding="utf-8")
        monkeypatch.setattr(mod, "ROOTS_CONFIG", roots_file)
        mod._RESOLVED_URL_CACHE.clear()

    def test_notes_path_uses_sibling_directory(tmp_path):
        source = tmp_path / "reports" / "paper.md"
        source.parent.mkdir(parents=True)
        source.write_text("# Paper\n", encoding="utf-8")

        notes = mod.notes_path_for(source)
        assert notes == source.parent / "paper_notes" / "paper_notes.md"

    def test_resolve_by_hints_prefers_exact_stem(monkeypatch, tmp_path):
        _set_roots(monkeypatch, tmp_path)

        (tmp_path / "a").mkdir()
        (tmp_path / "b").mkdir()
        index = tmp_path / "a" / "index.md"
        foster = tmp_path / "b" / "Foster_et_al_2013_Human_retrosplenial_cortex_displays_transient_thet_no_refs.md"
        index.write_text("# Index\n", encoding="utf-8")
        foster.write_text("# Foster\n", encoding="utf-8")

        resolved = mod._resolve_by_hints(
            ["Foster_et_al_2013_Human_retrosplenial_cortex_displays_transient_thet_no_refs"]
        )
        assert resolved == foster

    def test_append_capture_creates_directory_and_file(monkeypatch, tmp_path):
        _set_roots(monkeypatch, tmp_path)

        source = tmp_path / "reports" / "paper.md"
        source.parent.mkdir(parents=True)
        source.write_text("# Paper\n", encoding="utf-8")

        notes_path, source_path = mod.append_capture(
            "This is captured.",
            "http://localhost:4444/reports/paper.html",
            ["paper"],
        )

        assert notes_path == source.parent / "paper_notes" / "paper_notes.md"
        assert source_path == source
        content = notes_path.read_text(encoding="utf-8")
        assert "**Source**: [paper.md](../paper.md)" in content
        assert "> This is captured." in content

    def test_append_capture_resolves_root_url_from_title_hint(monkeypatch, tmp_path):
        _set_roots(monkeypatch, tmp_path)

        source = (
            tmp_path
            / "Foster_et_al_2013_Human_retrosplenial_cortex_displays_transient_thet"
            / "Foster_et_al_2013_Human_retrosplenial_cortex_displays_transient_thet_no_refs.md"
        )
        source.parent.mkdir(parents=True)
        source.write_text("# Foster\n", encoding="utf-8")

        notes_path, source_path = mod.append_capture(
            "Captured from root url.",
            "http://localhost:4444/",
            ["index", "foster_et_al_2013_human_retrosplenial_cortex_displays_transient_thet_no_refs"],
        )

        assert notes_path == source.parent / (
            "Foster_et_al_2013_Human_retrosplenial_cortex_displays_transient_thet_no_refs_notes"
        ) / (
            "Foster_et_al_2013_Human_retrosplenial_cortex_displays_transient_thet_no_refs_notes.md"
        )
        assert source_path == source
        content = notes_path.read_text(encoding="utf-8")
        assert "> Captured from root url." in content

    def test_append_capture_logs_success(monkeypatch, tmp_path):
        _set_roots(monkeypatch, tmp_path)
        log_file = tmp_path / "preview_sync.log"
        monkeypatch.setattr(mod, "LOG_FILE", log_file)

        source = tmp_path / "reports" / "paper.md"
        source.parent.mkdir(parents=True)
        source.write_text("# Paper\n", encoding="utf-8")

        mod.append_capture(
            "Log this capture.",
            "http://localhost:4444/reports/paper.html",
            ["paper"],
        )

        logged = log_file.read_text(encoding="utf-8")
        assert "capture_ok" in logged
        assert "Log this capture." in logged
        assert "reports/paper.md" in logged

    def test_scope_normalization():
        assert mod._sanitize_scope("http://LOCALHOST:6806", "") == "http://localhost:6806"
        assert mod._sanitize_scope("", "http://127.0.0.1:4444/index.html") == "http://127.0.0.1:4444"
        assert mod._sanitize_scope("bad://scope", "http://localhost:7000/x") == "http://localhost:7000"

    def test_pinned_source_roundtrip(tmp_path):
        source = tmp_path / "doc.md"
        source.write_text("# doc\n", encoding="utf-8")
        scope = "http://localhost:6806"

        mod._clear_pinned_source()
        mod._set_pinned_source(scope, source)
        assert mod._get_pinned_source(scope) == source
        mod._clear_pinned_source(scope)
        assert mod._get_pinned_source(scope) is None

    def test_append_capture_uses_pinned_source(monkeypatch, tmp_path):
        _set_roots(monkeypatch, tmp_path)
        source_a = tmp_path / "A.md"
        source_b = tmp_path / "B.md"
        source_a.write_text("# A\n", encoding="utf-8")
        source_b.write_text("# B\n", encoding="utf-8")

        notes_path, source_path = mod.append_capture(
            "Pinned capture sentence",
            "http://localhost:6806/",
            ["A"],
            pinned_source=source_b,
        )

        assert source_path == source_b
        assert notes_path == tmp_path / "B_notes" / "B_notes.md"
        content = notes_path.read_text(encoding="utf-8")
        assert "> Pinned capture sentence" in content

    def test_origin_allowlist():
        assert mod._is_allowed_origin("http://localhost:4444") is True
        assert mod._is_allowed_origin("http://127.0.0.1:4000") is True
        assert mod._is_allowed_origin("https://example.com") is False
        assert mod._is_allowed_origin("file:///tmp/x") is False

    def test_source_hint_sanitization():
        hints = mod._sanitize_source_hints(
            ["  foster  ", "", 42, "x" * 999]
        )
        assert hints[0] == "foster"
        assert len(hints[1]) == mod.MAX_HINT_CHARS
