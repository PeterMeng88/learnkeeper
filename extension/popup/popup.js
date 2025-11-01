let currentTab = null;
let pageContent = "";

// 保存历史记录
async function saveToHistory(data) {
  const history = await chrome.storage.local.get('saveHistory') || { saveHistory: [] };
  const historyList = history.saveHistory || [];
  
  historyList.unshift({
    title: data.title,
    url: data.url,
    timestamp: new Date().toISOString(),
    tags: data.tags
  });
  
  // 只保留最近50条
  if (historyList.length > 50) {
    historyList.pop();
  }
  
  await chrome.storage.local.set({ saveHistory: historyList });
}

// 页面加载时获取标签页信息
document.addEventListener('DOMContentLoaded', async () => {
  console.log("Popup loaded");
  
  // 加载最近使用的标签
  const recent = await chrome.storage.local.get('recentTags');
  if (recent.recentTags && recent.recentTags.length > 0) {
    document.getElementById('tags-input').placeholder = 
      `常用标签：${recent.recentTags.slice(0, 3).join(', ')}`;
  }
  
  try {
    const tabs = await chrome.tabs.query({active: true, currentWindow: true});
    currentTab = tabs[0];
    
    console.log("当前标签页:", currentTab);
    
    document.getElementById('title').textContent = currentTab.title || "无标题";
    document.getElementById('url').textContent = currentTab.url || "无URL";
    
    try {
      await chrome.scripting.executeScript({
        target: { tabId: currentTab.id },
        files: ['content.js']
      });
      console.log("Content script 注入成功");
    } catch (e) {
      console.log("Content script 可能已注入:", e);
    }
    
    setTimeout(async () => {
      try {
        const response = await chrome.tabs.sendMessage(currentTab.id, {
          action: "getContent"
        });
        
        if (response && response.content) {
          pageContent = response.content;
          console.log("获取到内容，长度:", pageContent.length);
          
          // 如果有metadata，显示来源类型
          if (response.metadata && response.metadata.source) {
            const sourceTag = document.createElement('span');
            sourceTag.style.cssText = 'background:#667eea;color:white;padding:2px 8px;border-radius:4px;font-size:11px;margin-left:8px;';
            sourceTag.textContent = response.metadata.source;
            document.getElementById('title').appendChild(sourceTag);
          }
        } else {
          console.log("没有收到内容响应");
          pageContent = "无法提取页面内容";
        }
      } catch (error) {
        console.error("发送消息失败:", error);
        pageContent = "无法提取页面内容";
      }
    }, 500);
    
  } catch (error) {
    console.error("初始化失败:", error);
    document.getElementById('title').textContent = "获取失败";
    document.getElementById('url').textContent = error.message;
  }
});

// 保存按钮点击
document.getElementById('save-btn').addEventListener('click', async () => {
  console.log("点击保存按钮");
  
  const title = document.getElementById('title').textContent;
  const url = document.getElementById('url').textContent;
  const notes = document.getElementById('notes').value;
  const tagsInput = document.getElementById('tags-input').value;
  const tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);
  
  const statusDiv = document.getElementById('status');
  const saveBtn = document.getElementById('save-btn');
  
  saveBtn.disabled = true;
  statusDiv.textContent = '🔄 处理中...';
  statusDiv.style.color = '#666';
  
  console.log("准备发送数据:", { title, url, notes, tags });
  
  try {
    const response = await fetch('http://localhost:8000/api/save-content', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: title,
        url: url,
        content: pageContent || "无内容",
        notes: notes,
        tags: tags,
        vault_path: "",  // 用户需自行配置
        metadata: {}
      })
    });
    
    console.log("响应状态:", response.status);
    const result = await response.json();
    console.log("响应数据:", result);
    
    if (result.success) {
      // 保存到历史
      await saveToHistory({ title, url, tags });
      
      // 更新常用标签
      if (tags.length > 0) {
        const recent = await chrome.storage.local.get('recentTags');
        let recentTags = recent.recentTags || [];
        tags.forEach(tag => {
          recentTags = recentTags.filter(t => t !== tag);
          recentTags.unshift(tag);
        });
        await chrome.storage.local.set({ recentTags: recentTags.slice(0, 10) });
      }
      
      statusDiv.textContent = '✅ 已保存到知识库';
      statusDiv.style.color = 'green';
      statusDiv.style.background = '#e8f5e9';
      
      // 显示AI建议的标签
      if (result.suggested_tags && result.suggested_tags.length > 0) {
        statusDiv.textContent += ` | AI建议标签: ${result.suggested_tags.join(', ')}`;
      }
      
      setTimeout(() => window.close(), 2000);
    } else {
      statusDiv.textContent = '❌ ' + (result.message || '保存失败');
      statusDiv.style.color = 'red';
      statusDiv.style.background = '#ffebee';
      saveBtn.disabled = false;
    }
  } catch (error) {
    console.error("保存失败:", error);
    statusDiv.textContent = '❌ 连接失败: ' + error.message;
    statusDiv.style.color = 'red';
    statusDiv.style.background = '#ffebee';
    saveBtn.disabled = false;
  }
});
