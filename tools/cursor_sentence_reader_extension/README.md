# Cursor Sentence Reader Extension

Reads the active document sentence-by-sentence using macOS `say` while selecting the current sentence in Cursor.

Commands contributed:

- `rebeccaSentenceReader.start`
- `rebeccaSentenceReader.stop`
- `rebeccaSentenceReader.captureCurrentSentenceToNotes`

Notes capture writes to a sibling file named `*_notes.md` beside the current file and appends blockquotes.

Each capture now includes a backlink line with:
- source file + line link (`file.md#L<line>`)
- nearest markdown heading link (`file.md#<heading-slug>`) when available
