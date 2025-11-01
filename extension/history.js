async function loadHistory() {
  const result = await chrome.storage.local.get('saveHistory');
  const history = result.saveHistory || [];
  const listDiv = document.getElementById('history-list');
  
  if (history.length === 0) {
    listDiv.innerHTML = '<div class="empty">暂无保存记录</div>';
    return;
  }
  
  listDiv.innerHTML = history.map(item => `
    <div class="history-item" data-url="${item.url}">
      <div class="history-title">${item.title}</div>
      <div class="history-meta">
        ${new Date(item.timestamp).toLocaleString('zh-CN')}
      </div>
      ${item.tags && item.tags.length > 0 ? `
        <div class="history-tags">
          ${item.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
        </div>
      ` : ''}
    </div>
  `).join('');
  
  // 点击跳转
  document.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
      const url = item.dataset.url;
      chrome.tabs.create({ url: url });
    });
  });
}

loadHistory();
