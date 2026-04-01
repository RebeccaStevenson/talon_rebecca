# Preview Sync Chrome Extension

This extension enables sentence-by-sentence reading + highlighting on localhost preview pages and capture-to-notes via the local Talon server.

## Install (Developer Mode)

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select:
   - `/Users/rebec/.talon/user/talon_rebecca/tools/preview_sync/preview_sync_chrome_extension`

## Shortcuts

Default shortcuts (macOS):
- Start premium/system reading: `cmd-shift-7`
- Start reading: `cmd-shift-8`
- Stop reading: `cmd-shift-9`
- Capture current sentence: `cmd-shift-u`

You can customize in `chrome://extensions/shortcuts`.

## Capture behavior

- If the page currently has selected text, capture uses that selected sentence first.
- Otherwise, capture uses the extension's currently highlighted sentence.
- This keeps capture working when sentence highlighting is driven by browser/system selection.
- Before each capture, the extension pins the current preview source (by `window.location.origin`)
  and capture uses that pinned source to avoid cross-document drift.

## Notes path mapping

Captures are posted to `http://127.0.0.1:27832/capture`.
The server resolves source paths from localhost URLs using configured roots in:

- `~/.talon/user/talon_rebecca_personal/settings/preview_sync_roots.json` (preferred)
- `talon_rebecca/settings/preview_sync_roots.json` (fallback)

Example config:

```json
{
  "roots": [
    "/Users/rebec/localFiles",
    "/Users/rebec/localFiles/notes"
  ]
}
```

For URL `/reports/paper.html`, resolver tries:
- `<root>/reports/paper.qmd`
- `<root>/reports/paper.md`
- and `_site`-stripped variants.
