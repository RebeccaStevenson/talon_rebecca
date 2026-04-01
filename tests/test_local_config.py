"""Tests for shared local/private config helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.core.local_config as local_config

    def test_load_first_json_object_prefers_first_valid_file(tmp_path):
        private = tmp_path / "private.json"
        public = tmp_path / "public.json"
        private.write_text('{"preferred": "private"}\n', encoding="utf-8")
        public.write_text('{"preferred": "public"}\n', encoding="utf-8")

        config = local_config.load_first_json_object((private, public))

        assert config == {"preferred": "private"}

    def test_load_first_json_object_skips_invalid_json(tmp_path):
        invalid = tmp_path / "invalid.json"
        valid = tmp_path / "valid.json"
        invalid.write_text("{not valid json}\n", encoding="utf-8")
        valid.write_text('{"ok": true}\n', encoding="utf-8")

        config = local_config.load_first_json_object((invalid, valid))

        assert config == {"ok": True}

    def test_ensure_json_file_creates_parent_dirs(tmp_path):
        config_path = tmp_path / "nested" / "config.json"

        local_config.ensure_json_file(config_path, {"roots": ["/tmp/example"]})

        assert config_path.exists()
        assert config_path.read_text(encoding="utf-8").endswith("\n")

    def test_configured_path_returns_expanded_path():
        config = {"example": "~/Documents/example"}

        path = local_config.configured_path(config, "example")

        assert path is not None
        assert str(path).endswith("/Documents/example")
