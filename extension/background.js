// 安装时显示引导页
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    chrome.tabs.create({
      url: 'onboarding.html'
    });
  }
  
  // 创建右键菜单
  chrome.contextMenus.create({
    id: "saveToKB",
    title: "保存到知识库",
    contexts: ["selection", "page"]
  });
  
  chrome.contextMenus.create({
    id: "viewHistory",
    title: "查看保存历史",
    contexts: ["action"]
  });
  
  console.log("知识库插件已安装");
});

// 右键菜单点击
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "saveToKB") {
    chrome.action.openPopup();
  } else if (info.menuItemId === "viewHistory") {
    chrome.tabs.create({ url: chrome.runtime.getURL('history.html') });
  }
});

// 快捷键处理（其他代码...）
