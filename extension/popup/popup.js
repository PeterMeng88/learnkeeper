let currentTab = null;
let pageContent = "";

// 页面加载时获取标签页信息
document.addEventListener('DOMContentLoaded', async () => {
  console.log("Popup loaded");
  
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
  
  try {
    // 尝试调用后端获取AI摘要
    let aiSummary = '';
    let keyPoints = [];
    let suggestedTags = [];
    
    try {
      const response = await fetch('http://localhost:8000/api/save-content', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          title: title,
          url: url,
          content: pageContent || "无内容",
          notes: notes,
          tags: tags,
          vault_path: "",
          metadata: {}
        }),
        signal: AbortSignal.timeout(5000)
      });
      
      if (response.ok) {
        const result = await response.json();
        if (result.success && result.ai_enhanced) {
          aiSummary = result.summary || '';
          keyPoints = result.key_points || [];
          suggestedTags = result.suggested_tags || [];
        }
      }
    } catch (error) {
      console.log("后端不可用，使用本地保存:", error);
    }
    
    // 合并标签
    const allTags = [...new Set([...tags, ...suggestedTags])];
    
    // 生成Markdown内容
    const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
    const markdown = `---
title: ${title}
url: ${url}
tags: ${allTags.join(', ')}
created: ${new Date().toLocaleString('zh-CN')}
---

# ${title}

## 🔗 原文链接
${url}

${aiSummary ? `## 📝 AI摘要
${aiSummary}

` : ''}${keyPoints.length > 0 ? `## 💡 关键知识点
${keyPoints.map((p, i) => `${i + 1}. ${p}`).join('\n')}

` : ''}${notes ? `## ✍️ 个人笔记
${notes}

` : ''}## 📄 原文内容

${pageContent ? pageContent.substring(0, 5000) : '无法提取内容'}${pageContent && pageContent.length > 5000 ? '...' : ''}

---
> 💾 由 LearnKeeper 保存  
> ⏰ ${new Date().toLocaleString('zh-CN')}
`;
    
    // 生成文件名
    const safeTitle = title.replace(/[\\/*?:"<>|]/g, '').substring(0, 50);
    const filename = `LearnKeeper/${safeTitle}_${timestamp}.md`;
    
    // 下载文件
    const blob = new Blob([markdown], {type: 'text/markdown; charset=utf-8'});
    const downloadUrl = URL.createObjectURL(blob);
    
    chrome.downloads.download({
      url: downloadUrl,
      filename: filename,
      saveAs: false
    }, (downloadId) => {
      if (chrome.runtime.lastError) {
        statusDiv.textContent = '❌ 保存失败: ' + chrome.runtime.lastError.message;
        statusDiv.style.color = 'red';
        saveBtn.disabled = false;
      } else {
        statusDiv.textContent = '✅ 已保存到下载文件夹/LearnKeeper';
        statusDiv.style.color = 'green';
        
        if (suggestedTags.length > 0) {
          statusDiv.textContent += ` | AI: ${suggestedTags.slice(0, 3).join(', ')}`;
        }
        
        setTimeout(() => window.close(), 2000);
      }
      
      URL.revokeObjectURL(downloadUrl);
    });
    
  } catch (error) {
    console.error("保存失败:", error);
    statusDiv.textContent = '❌ 保存失败: ' + error.message;
    statusDiv.style.color = 'red';
    saveBtn.disabled = false;
  }
});
