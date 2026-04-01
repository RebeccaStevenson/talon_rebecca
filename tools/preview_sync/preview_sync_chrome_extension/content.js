(function () {
  const HIGHLIGHT_CLASS = 'preview-sync-current-sentence';
  const CAPTURE_URL = 'http://127.0.0.1:27832/capture';
  const PIN_URL = 'http://127.0.0.1:27832/pin_source';
  const SPEAK_URL = 'http://127.0.0.1:27832/speak';
  const SPEAK_STATUS_URL = 'http://127.0.0.1:27832/speak_status';
  const SPEAK_STOP_URL = 'http://127.0.0.1:27832/speak_stop';

  const state = {
    spans: [],
    index: -1,
    running: false,
    utterance: null,
    mode: 'web',
  };

  function showToast(message, kind = 'info') {
    const existing = document.getElementById('preview-sync-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'preview-sync-toast';
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.right = '18px';
    toast.style.bottom = '18px';
    toast.style.zIndex = '2147483647';
    toast.style.padding = '10px 12px';
    toast.style.borderRadius = '8px';
    toast.style.fontSize = '13px';
    toast.style.fontFamily = 'ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif';
    toast.style.color = '#111111';
    toast.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.22)';
    toast.style.background = kind === 'error' ? '#ffd7d7' : '#d6f7dd';
    toast.style.border = kind === 'error' ? '1px solid #ef8d8d' : '1px solid #8ccf9a';
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 2600);
  }

  function sentenceSegments(text) {
    if (!text || !text.trim()) return [];

    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
      const seg = new Intl.Segmenter('en', { granularity: 'sentence' });
      return Array.from(seg.segment(text)).map((s) => ({
        index: s.index,
        segment: s.segment,
      }));
    }

    const out = [];
    const re = /[^.!?\n]+[.!?]?|\n+/g;
    let m;
    while ((m = re.exec(text)) !== null) {
      out.push({ index: m.index, segment: m[0] });
    }
    return out;
  }

  function clearMarkers() {
    for (const span of state.spans) {
      span.classList.remove(HIGHLIGHT_CLASS);
    }
  }

  function pickRoot() {
    return (
      document.querySelector('#quarto-document-content') ||
      document.querySelector('main') ||
      document.body
    );
  }

  function buildSentenceSpans() {
    const root = pickRoot();
    if (!root) return [];

    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          const parent = node.parentElement;
          if (!parent) return NodeFilter.FILTER_REJECT;
          const tag = parent.tagName;
          if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEXTAREA'].includes(tag)) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        },
      }
    );

    const textNodes = [];
    let node;
    while ((node = walker.nextNode())) {
      textNodes.push(node);
    }

    const spans = [];

    for (const textNode of textNodes) {
      const text = textNode.nodeValue;
      const segs = sentenceSegments(text);
      if (!segs.length) continue;

      const frag = document.createDocumentFragment();
      let cursor = 0;

      for (const seg of segs) {
        const segStart = seg.index;
        const segEnd = seg.index + seg.segment.length;

        if (segStart > cursor) {
          frag.appendChild(document.createTextNode(text.slice(cursor, segStart)));
        }

        const sentenceText = text.slice(segStart, segEnd);
        const clean = sentenceText.trim();
        if (clean) {
          const span = document.createElement('span');
          span.textContent = sentenceText;
          span.dataset.previewSyncSentence = '1';
          frag.appendChild(span);
          spans.push(span);
        } else {
          frag.appendChild(document.createTextNode(sentenceText));
        }

        cursor = segEnd;
      }

      if (cursor < text.length) {
        frag.appendChild(document.createTextNode(text.slice(cursor)));
      }

      textNode.parentNode.replaceChild(frag, textNode);
    }

    return spans;
  }

  function sentenceIndexFromSelection() {
    const sel = window.getSelection();
    if (!sel || sel.rangeCount === 0) return -1;
    const anchor = sel.anchorNode;
    if (!anchor) return -1;

    const element = anchor.nodeType === Node.TEXT_NODE ? anchor.parentElement : anchor;
    if (!element) return -1;

    const span = element.closest('span[data-preview-sync-sentence="1"]');
    if (!span) return -1;

    return state.spans.indexOf(span);
  }

  function sentenceIndexNearViewport() {
    const viewportMid = window.innerHeight * 0.35;
    for (let i = 0; i < state.spans.length; i += 1) {
      const rect = state.spans[i].getBoundingClientRect();
      if (rect.bottom >= viewportMid) return i;
    }
    return state.spans.length ? 0 : -1;
  }

  function focusSentence(index) {
    if (index < 0 || index >= state.spans.length) return null;

    clearMarkers();
    const span = state.spans[index];
    span.classList.add(HIGHLIGHT_CLASS);
    span.scrollIntoView({ block: 'center', behavior: 'smooth' });
    state.index = index;
    return span;
  }

  function stopReading() {
    state.running = false;
    if (state.utterance) {
      window.speechSynthesis.cancel();
      state.utterance = null;
    }
    if (state.mode === 'system') {
      fetch(SPEAK_STOP_URL, { method: 'POST' }).catch(() => {});
    }
  }

  function speakCurrentThenAdvance() {
    if (!state.running) return;

    const span = focusSentence(state.index);
    if (!span) {
      stopReading();
      return;
    }

    const text = span.textContent.trim();
    if (!text) {
      state.index += 1;
      setTimeout(speakCurrentThenAdvance, 10);
      return;
    }

    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1.0;
    utter.pitch = 1.0;

    utter.onend = () => {
      if (!state.running) return;
      state.index += 1;
      setTimeout(speakCurrentThenAdvance, 35);
    };

    utter.onerror = () => {
      stopReading();
    };

    state.utterance = utter;
    window.speechSynthesis.speak(utter);
  }

  async function speakViaSystemVoice(sentence) {
    const resp = await fetch(SPEAK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sentence }),
    });
    const payload = await resp.json();
    return resp.ok && payload.ok;
  }

  async function waitForSystemVoiceDone(maxMs = 120000) {
    const start = Date.now();
    while (state.running) {
      let speaking = false;
      try {
        const resp = await fetch(SPEAK_STATUS_URL, { method: 'GET' });
        const payload = await resp.json();
        speaking = Boolean(resp.ok && payload.ok && payload.speaking);
      } catch (_) {
        return false;
      }

      if (!speaking) return true;
      if (Date.now() - start > maxMs) return false;
      await new Promise((resolve) => setTimeout(resolve, 120));
    }
    return false;
  }

  async function speakCurrentThenAdvanceSystem() {
    if (!state.running) return;

    const span = focusSentence(state.index);
    if (!span) {
      stopReading();
      return;
    }

    const text = span.textContent.trim();
    if (!text) {
      state.index += 1;
      setTimeout(speakCurrentThenAdvanceSystem, 10);
      return;
    }

    const started = await speakViaSystemVoice(text);
    if (!started) {
      stopReading();
      return;
    }

    const completed = await waitForSystemVoiceDone();
    if (!state.running) return;
    if (!completed) {
      stopReading();
      return;
    }

    state.index += 1;
    setTimeout(speakCurrentThenAdvanceSystem, 35);
  }

  function ensureSpans() {
    if (!state.spans.length) {
      state.spans = buildSentenceSpans();
    }
    return state.spans.length > 0;
  }

  function sourceHintsForPage() {
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const pathName = pathParts.length ? pathParts[pathParts.length - 1] : '';
    const pathStem = pathName ? pathName.replace(/\.[^/.]+$/, '') : '';
    const titleStem = (document.title || '').trim().replace(/\.[^/.]+$/, '');
    return [pathStem, titleStem].filter(Boolean);
  }

  async function pinCurrentSource() {
    const sourceHints = sourceHintsForPage();
    const resp = await fetch(PIN_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pageUrl: window.location.href,
        title: document.title,
        sourceHints,
        scope: window.location.origin,
      }),
    });
    const payload = await resp.json();
    if (!resp.ok || !payload.ok) {
      throw new Error(payload.error || 'pin failed');
    }
    return payload;
  }

  function startReading(mode = 'web') {
    stopReading();
    if (!ensureSpans()) return;

    pinCurrentSource().catch((err) => {
      console.warn('Preview sync source pin failed:', err);
    });

    const selIndex = sentenceIndexFromSelection();
    state.index = selIndex >= 0 ? selIndex : sentenceIndexNearViewport();
    if (state.index < 0) return;

    state.running = true;
    state.mode = mode;
    if (mode === 'system') {
      speakCurrentThenAdvanceSystem();
      return;
    }
    speakCurrentThenAdvance();
  }

  async function captureCurrentSentence() {
    const selectedText = (window.getSelection && window.getSelection().toString().trim()) || '';
    let sentenceFromSelection = '';
    if (selectedText) {
      const segments = sentenceSegments(selectedText)
        .map((seg) => (seg.segment || '').trim())
        .filter(Boolean);
      sentenceFromSelection = segments.length ? segments[0] : selectedText;
    }

    if (!sentenceFromSelection && !ensureSpans()) {
      showToast('Capture failed: no readable text found on page', 'error');
      return;
    }

    // Prefer the sentence currently highlighted in the DOM so capture matches
    // what the user sees, even during brief reader index transitions.
    let span = null;
    let idx = -1;
    if (!sentenceFromSelection) {
      span = document.querySelector(`span[data-preview-sync-sentence="1"].${HIGHLIGHT_CLASS}`);
      idx = span ? state.spans.indexOf(span) : -1;
    }

    if (!sentenceFromSelection && !span) {
      idx = state.index;
      if (idx < 0) {
        const selIndex = sentenceIndexFromSelection();
        idx = selIndex >= 0 ? selIndex : sentenceIndexNearViewport();
      }
      if (idx < 0 || idx >= state.spans.length) {
        showToast('Capture failed: no current sentence available', 'error');
        return;
      }
      span = state.spans[idx];
    }

    const sentence = (sentenceFromSelection || (span && span.textContent) || '').trim();
    if (!sentence) {
      showToast('Capture failed: current sentence is empty', 'error');
      return;
    }

    if (!sentenceFromSelection) {
      focusSentence(idx);
    }

    const sourceHints = sourceHintsForPage();

    try {
      try {
        await pinCurrentSource();
      } catch (pinErr) {
        console.warn('Preview sync source pin failed before capture:', pinErr);
      }

      const resp = await fetch(CAPTURE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sentence,
          pageUrl: window.location.href,
          title: document.title,
          sourceHints,
          scope: window.location.origin,
          usePinned: true,
        }),
      });

      const payload = await resp.json();
      if (!resp.ok || !payload.ok) {
        console.warn('Preview sync capture failed:', payload);
        showToast(`Capture failed: ${payload.error || 'unknown error'}`, 'error');
        return;
      }
      showToast(`Captured to ${payload.notesFile || 'notes file'}`);
    } catch (err) {
      console.warn('Preview sync capture request error:', err);
      showToast('Capture failed: cannot reach local capture server', 'error');
    }
  }

  chrome.runtime.onMessage.addListener((message) => {
    if (!message || !message.action) return;
    if (message.action === 'start') startReading();
    if (message.action === 'start_system') startReading('system');
    if (message.action === 'stop') stopReading();
    if (message.action === 'capture') captureCurrentSentence();
  });
})();
