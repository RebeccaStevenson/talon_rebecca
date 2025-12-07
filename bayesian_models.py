from pathlib import Path
from talon import Module, actions, app

mod = Module()

_BAYESIAN_MODELS_ROOT = Path("/Users/rebec/localFiles/reversal_python/data/bayesian_models")


def _latest_subfolder(root: Path) -> Path | None:
    """Return the most recently modified subdirectory under root."""
    most_recent: tuple[float, Path] | None = None
    for child in root.iterdir():
        if not child.is_dir():
            continue
        try:
            modified = child.stat().st_mtime
        except OSError:
            continue
        if most_recent is None or modified > most_recent[0]:
            most_recent = (modified, child)
    return most_recent[1] if most_recent else None


@mod.action_class
class Actions:
    def open_recent_bayesian_models_folder():
        """Open the most recently modified Bayesian models subfolder."""
        if not _BAYESIAN_MODELS_ROOT.exists():
            app.notify("Bayesian models directory missing")
            return

        latest = _latest_subfolder(_BAYESIAN_MODELS_ROOT)
        if latest is None:
            app.notify("No Bayesian model subfolders found")
            return

        actions.app.notify(f"Opening {latest.name}")
        actions.user.open_file_custom(str(latest))

    def open_recent_bayesian_diagnostics_folder():
        """Open the diagnostics subfolder from the most recent Bayesian result."""
        if not _BAYESIAN_MODELS_ROOT.exists():
            app.notify("Bayesian models directory missing")
            return

        latest = _latest_subfolder(_BAYESIAN_MODELS_ROOT)
        if latest is None:
            app.notify("No Bayesian model subfolders found")
            return

        diagnostics_path = latest / "diagnostics"
        if not diagnostics_path.is_dir():
            app.notify(f"No diagnostics folder in {latest.name}")
            return

        actions.app.notify(f"Opening diagnostics for {latest.name}")
        actions.user.open_file_custom(str(diagnostics_path))
