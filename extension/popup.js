document.getElementById('download').addEventListener('click', async () => {
  const url = document.getElementById('url').value.trim();
  const format = document.getElementById('format').value;
  const button = document.getElementById('download');
  const status = document.getElementById('status');

  if (!url) {
    showStatus('Please enter a YouTube URL', 'error');
    return;
  }

  button.disabled = true;
  button.textContent = 'Downloading...';
  status.style.display = 'none';

  try {
    const response = await fetch('http://localhost:5000/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, format })
    });

    if (!response.ok) {
      const data = await response.json();
      showStatus(`✗ Error: ${data.error}`, 'error');
      return;
    }

    const blob = await response.blob();
    const disposition = response.headers.get('content-disposition');
    let filename = `video.${format === 'MP3' ? 'm4a' : 'mp4'}`;
    
    if (disposition) {
      const matches = disposition.match(/filename="?(.+?)"?$/i);
      if (matches) filename = matches[1];
    }

    const downloadUrl = URL.createObjectURL(blob);
    
    chrome.downloads.download({
      url: downloadUrl,
      filename: filename,
      saveAs: false
    }, (downloadId) => {
      if (downloadId) {
        showStatus(`✓ Downloaded: ${filename}`, 'success');
        document.getElementById('url').value = '';
      } else {
        showStatus('✗ Download failed', 'error');
      }
      setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
    });
  } catch (error) {
    showStatus('✗ Cannot connect to backend. Make sure server.py is running!', 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'Download';
  }
});

function showStatus(message, type) {
  const status = document.getElementById('status');
  status.textContent = message;
  status.className = type;
  status.style.display = 'block';
}
