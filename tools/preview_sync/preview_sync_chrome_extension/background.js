const COMMAND_TO_ACTION = {
  'preview-sync-start-system': 'start_system',
  'preview-sync-start': 'start',
  'preview-sync-stop': 'stop',
  'preview-sync-capture': 'capture',
};

async function sendToActiveTab(action) {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const tab = tabs && tabs[0];
  if (!tab || !tab.id) return;

  try {
    await chrome.tabs.sendMessage(tab.id, { action });
  } catch (_) {
    // Content script may not be available for this tab.
  }
}

chrome.commands.onCommand.addListener((command) => {
  const action = COMMAND_TO_ACTION[command];
  if (!action) return;
  sendToActiveTab(action);
});
