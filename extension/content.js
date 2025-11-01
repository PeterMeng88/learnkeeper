console.log("Content script loaded");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getContent") {
    const pageInfo = extractPageInfo();
    console.log("提取的内容长度:", pageInfo.content.length);
    sendResponse(pageInfo);
  }
  return true;
});

function extractPageInfo() {
  const url = window.location.href;
  
  // 根据不同网站使用不同提取策略
  if (url.includes('baike.baidu.com')) {
    return extractBaidu();
  } else if (url.includes('zhihu.com')) {
    return extractZhihu();
  } else if (url.includes('juejin.cn')) {
    return extractJuejin();
  } else if (url.includes('csdn.net')) {
    return extractCSDN();
  } else if (url.includes('mp.weixin.qq.com')) {
    return extractWeixin();
  } else if (url.includes('youtube.com') || url.includes('bilibili.com')) {
    return extractVideo();
  } else {
    return extractGeneral();
  }
}

// 百度百科
function extractBaidu() {
  const title = document.querySelector('.lemmaWgt-lemmaTitle-title h1')?.innerText || document.title;
  const summary = document.querySelector('.lemma-summary')?.innerText || '';
  const content = document.querySelector('.lemmaWgt-content')?.innerText || document.body.innerText;
  
  return {
    content: `# 摘要\n${summary}\n\n# 详细内容\n${content}`,
    metadata: {
      source: '百度百科',
      type: '百科词条'
    }
  };
}

// 知乎
function extractZhihu() {
  const title = document.querySelector('.QuestionHeader-title')?.innerText || document.title;
  const question = document.querySelector('.QuestionRichText')?.innerText || '';
  const answers = Array.from(document.querySelectorAll('.RichContent-inner'))
    .slice(0, 3)
    .map(a => a.innerText)
    .join('\n\n---\n\n');
  
  return {
    content: `# 问题\n${question}\n\n# 高赞回答\n${answers}`,
    metadata: {
      source: '知乎',
      type: '问答'
    }
  };
}

// 掘金
function extractJuejin() {
  const title = document.querySelector('.article-title')?.innerText || document.title;
  const content = document.querySelector('.markdown-body')?.innerText || '';
  
  return {
    content: content,
    metadata: {
      source: '掘金',
      type: '技术文章'
    }
  };
}

// CSDN
function extractCSDN() {
  const content = document.querySelector('#article_content')?.innerText || 
                 document.querySelector('.article-content')?.innerText || '';
  
  return {
    content: content,
    metadata: {
      source: 'CSDN',
      type: '技术博客'
    }
  };
}

// 微信公众号
function extractWeixin() {
  const content = document.querySelector('#js_content')?.innerText || '';
  const author = document.querySelector('#js_name')?.innerText || '';
  
  return {
    content: content,
    metadata: {
      source: '微信公众号',
      author: author,
      type: '公众号文章'
    }
  };
}

// 视频网站
function extractVideo() {
  const title = document.querySelector('h1')?.innerText || document.title;
  const description = document.querySelector('.video-desc')?.innerText || 
                     document.querySelector('#v_desc')?.innerText || '';
  
  return {
    content: `# 视频信息\n标题: ${title}\n\n简介:\n${description}\n\n注：需要配合字幕提取工具获取完整内容`,
    metadata: {
      source: '视频网站',
      type: '视频'
    }
  };
}

// 通用提取
function extractGeneral() {
  const selectors = ['article', 'main', '[role="main"]', '.content', '.main-content', '#content'];
  
  for (let selector of selectors) {
    const element = document.querySelector(selector);
    if (element && element.innerText.length > 100) {
      return {
        content: element.innerText.trim(),
        metadata: {
          source: '网页',
          type: '通用'
        }
      };
    }
  }
  
  return {
    content: document.body.innerText.trim(),
    metadata: {
      source: '网页',
      type: '通用'
    }
  };
}
