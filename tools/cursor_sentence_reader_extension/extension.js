const vscode = require('vscode');
const cp = require('child_process');
const fs = require('fs');
const path = require('path');

let session = null;

function splitIntoSentences(text) {
  if (!text || !text.trim()) {
    return [];
  }

  if (typeof Intl !== 'undefined' && Intl.Segmenter) {
    const segmenter = new Intl.Segmenter('en', { granularity: 'sentence' });
    return Array.from(segmenter.segment(text)).map((s) => ({
      index: s.index,
      segment: s.segment,
    }));
  }

  const results = [];
  const regex = /[^.!?\n]+[.!?]?|\n+/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    results.push({ index: match.index, segment: match[0] });
  }
  return results;
}

function rangesForDocument(doc) {
  const text = doc.getText();
  const segments = splitIntoSentences(text);
  const ranges = [];

  for (const seg of segments) {
    let start = seg.index;
    let end = seg.index + seg.segment.length;

    while (start < end && /\s/.test(text[start])) start += 1;
    while (end > start && /\s/.test(text[end - 1])) end -= 1;

    if (end <= start) continue;

    ranges.push(
      new vscode.Range(doc.positionAt(start), doc.positionAt(end))
    );
  }

  return ranges;
}

function sentenceIndexForOffset(doc, ranges, offset) {
  for (let i = 0; i < ranges.length; i += 1) {
    const r = ranges[i];
    const start = doc.offsetAt(r.start);
    const end = doc.offsetAt(r.end);
    if (offset >= start && offset <= end) return i;
  }

  for (let i = 0; i < ranges.length; i += 1) {
    const start = doc.offsetAt(ranges[i].start);
    if (start >= offset) return i;
  }

  return ranges.length ? ranges.length - 1 : -1;
}

function deriveNotesPath(filePath) {
  const ext = path.extname(filePath) || '.md';
  const base = path.basename(filePath, ext);
  const normalizedBase = base.replace(/(_notes|_citation)$/i, '');
  return path.join(path.dirname(filePath), `${normalizedBase}_notes${ext}`);
}

function ensureNotesFile(sourcePath, notesPath) {
  if (fs.existsSync(notesPath)) return;

  const sourceName = path.basename(sourcePath);
  const base = path.basename(notesPath, path.extname(notesPath));
  const prettyTitle = base.replace(/_notes$/i, '').replace(/_/g, ' ').trim();

  const header = [
    `# Notes: ${prettyTitle}`,
    '',
    `**Source**: [${sourceName}](${sourceName})`,
    '**Tags**:',
    '',
    '---',
    '',
  ].join('\n');

  fs.writeFileSync(notesPath, header, { encoding: 'utf-8' });
}

function headingForLine(doc, lineNumber) {
  for (let i = lineNumber; i >= 0; i -= 1) {
    const line = doc.lineAt(i).text.trim();
    const match = line.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (!match) continue;
    const heading = match[2].trim();
    if (!heading) continue;
    return heading;
  }
  return '';
}

function slugifyHeading(heading) {
  return heading
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

function appendSentenceToNotes(doc, text, sentenceRange = null) {
  const filePath = doc.uri.fsPath;
  const notesPath = deriveNotesPath(filePath);
  ensureNotesFile(filePath, notesPath);

  const clean = text.replace(/\s+/g, ' ').trim();
  const sourceName = path.basename(filePath);
  const lineNumber = sentenceRange ? sentenceRange.start.line + 1 : 1;
  const sourceLink = `[${sourceName}:${lineNumber}](${sourceName}#L${lineNumber})`;

  const heading = headingForLine(doc, sentenceRange ? sentenceRange.start.line : 0);
  const headingPart = heading
    ? ` | heading: [${heading}](${sourceName}#${slugifyHeading(heading)})`
    : '';

  const entry = `> ${clean}\n>\n> source: ${sourceLink}${headingPart}\n\n`;
  fs.appendFileSync(notesPath, entry, { encoding: 'utf-8' });
  return notesPath;
}

function stopSession(showMessage = true) {
  if (session && session.proc && !session.proc.killed) {
    try {
      session.proc.kill('SIGTERM');
    } catch (_) {
      // Ignore cleanup errors.
    }
  }
  session = null;
  if (showMessage) {
    vscode.window.setStatusBarMessage('Sentence Reader stopped', 1600);
  }
}

function speakNextSentence(localSession) {
  if (!session || session !== localSession || session.stopped) {
    return;
  }

  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.uri.toString() !== session.docUri) {
    stopSession(false);
    vscode.window.showWarningMessage('Sentence Reader stopped: active editor changed');
    return;
  }

  if (session.index >= session.ranges.length) {
    stopSession(false);
    vscode.window.setStatusBarMessage('Sentence Reader finished', 1800);
    return;
  }

  const range = session.ranges[session.index];
  const sentence = editor.document.getText(range).trim();
  if (!sentence) {
    session.index += 1;
    setTimeout(() => speakNextSentence(localSession), 10);
    return;
  }

  session.currentRange = range;
  session.currentSentence = sentence;

  editor.selections = [new vscode.Selection(range.start, range.end)];
  editor.revealRange(range, vscode.TextEditorRevealType.InCenterIfOutsideViewport);

  const proc = cp.spawn('say', [sentence], {
    stdio: 'ignore',
  });

  session.proc = proc;

  proc.on('exit', () => {
    if (!session || session !== localSession || session.stopped) {
      return;
    }

    session.proc = null;
    session.index += 1;
    setTimeout(() => speakNextSentence(localSession), 25);
  });

  proc.on('error', (err) => {
    stopSession(false);
    vscode.window.showErrorMessage(`Sentence Reader failed to speak: ${err.message}`);
  });
}

function startReading() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor for Sentence Reader');
    return;
  }

  const doc = editor.document;
  if (doc.isUntitled || doc.uri.scheme !== 'file') {
    vscode.window.showWarningMessage('Sentence Reader requires a saved local file');
    return;
  }

  const ranges = rangesForDocument(doc);
  if (!ranges.length) {
    vscode.window.showWarningMessage('No readable sentences found');
    return;
  }

  const startIndex = sentenceIndexForOffset(doc, ranges, doc.offsetAt(editor.selection.active));
  if (startIndex < 0) {
    vscode.window.showWarningMessage('No sentence found at cursor');
    return;
  }

  stopSession(false);

  session = {
    docUri: doc.uri.toString(),
    ranges,
    index: startIndex,
    proc: null,
    stopped: false,
    currentRange: null,
    currentSentence: '',
  };

  vscode.window.setStatusBarMessage('Sentence Reader started', 1200);
  speakNextSentence(session);
}

function captureCurrentSentenceToNotes() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor for capture');
    return;
  }

  const doc = editor.document;
  if (doc.isUntitled || doc.uri.scheme !== 'file') {
    vscode.window.showWarningMessage('Capture requires a saved local file');
    return;
  }

  let sentence = '';
  let sentenceRange = null;

  if (
    session &&
    session.docUri === doc.uri.toString() &&
    session.currentSentence &&
    session.currentRange
  ) {
    sentence = session.currentSentence;
    sentenceRange = session.currentRange;
  } else {
    const ranges = rangesForDocument(doc);
    if (!ranges.length) {
      vscode.window.showWarningMessage('No sentence found to capture');
      return;
    }
    const cursorOffset = doc.offsetAt(editor.selection.active);
    const idx = sentenceIndexForOffset(doc, ranges, cursorOffset);
    if (idx < 0) {
      vscode.window.showWarningMessage('No sentence found to capture');
      return;
    }
    sentenceRange = ranges[idx];
    sentence = doc.getText(sentenceRange).trim();
  }

  if (!sentence) {
    vscode.window.showWarningMessage('No sentence found to capture');
    return;
  }

  try {
    const notesPath = appendSentenceToNotes(doc, sentence, sentenceRange);
    vscode.window.setStatusBarMessage(`Captured to ${path.basename(notesPath)}`, 2000);
  } catch (err) {
    vscode.window.showErrorMessage(`Failed to append notes: ${err.message}`);
  }
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('rebeccaSentenceReader.start', startReading)
  );
  context.subscriptions.push(
    vscode.commands.registerCommand('rebeccaSentenceReader.stop', () => stopSession(true))
  );
  context.subscriptions.push(
    vscode.commands.registerCommand(
      'rebeccaSentenceReader.captureCurrentSentenceToNotes',
      captureCurrentSentenceToNotes
    )
  );

  context.subscriptions.push({ dispose: () => stopSession(false) });
}

function deactivate() {
  stopSession(false);
}

module.exports = {
  activate,
  deactivate,
};
