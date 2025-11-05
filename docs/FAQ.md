# 常见问题 FAQ

## 📦 安装相关

### Q: 支持哪些浏览器？
**A:** 目前支持：
- ✅ Chrome
- ✅ Edge（基于Chromium）
- ✅ Brave
- ✅ Opera
- ❌ Firefox（暂不支持）
- ❌ Safari（暂不支持）

---

### Q: 安装后找不到插件图标？
**A:** 
1. 点击浏览器右上角的拼图图标🧩
2. 找到LearnKeeper
3. 点击📌图钉，固定到工具栏

---

### Q: 提示"清单文件缺失"？
**A:** 
- 确认选择的是**解压后的文件夹**
- 不要选择zip文件本身
- 文件夹内应该有manifest.json

---

## 💾 使用相关

### Q: 必须安装后端吗？
**A:** 
**不需要！**
- 不安装后端：可以正常保存网页
- 安装后端：额外获得AI摘要和知识点提取

---

### Q: 文件保存在哪里？
**A:** 
Windows: `C:\Users\你的用户名\Downloads\LearnKeeper\`  
Mac: `~/Downloads/LearnKeeper/`

---

### Q: 可以修改保存位置吗？
**A:** 
目前固定保存到下载文件夹。可以：
- 方法1：定期手动移动到Obsidian
- 方法2：设置Obsidian仓库为Downloads/LearnKeeper
- 未来版本会支持自定义路径

---

### Q: 保存的文件是什么格式？
**A:** 
Markdown (.md) 格式，包含：
- 标题、URL、标签
- AI摘要（如果启用）
- 关键知识点
- 你的个人笔记
- 原文内容

---

### Q: 某些网站保存失败？
**A:** 
已优化网站：
- ✅ 百度百科
- ✅ 知乎
- ✅ 掘金
- ✅ CSDN
- ✅ 微信公众号
- ✅ 大部分新闻网站

如果某网站不支持，请在GitHub提Issue

---

### Q: 可以保存视频吗？
**A:** 
目前保存视频页面信息，不保存视频本身。
未来会支持字幕提取。

---

## 🤖 AI功能相关

### Q: AI功能要付费吗？
**A:** 
需要自己的API密钥：
- 硅基流动：新用户有免费额度
- 每次调用约¥0.0001
- 保存1000次约¥0.1

---

### Q: 后端启动失败？
**A:** 
检查：
1. Python版本（需要3.8+）
   ```
   python --version
   ```
2. 依赖是否安装
   ```
   pip list | grep fastapi
   ```
3. API密钥是否正确（.env文件）

---

### Q: 提示"AI功能启动失败"？
**A:** 
常见原因：
- ❌ API密钥错误
- ❌ 网络无法访问api.siliconflow.cn
- ❌ 账户余额不足

解决：
1. 登录硅基流动查看密钥和余额
2. 检查网络连接
3. 重新复制密钥到.env

---

### Q: 不启动后端能用吗？
**A:** 
**完全可以！**
- 插件独立工作
- 只是没有AI摘要
- 手动添加笔记和标签

---

## 🔗 集成相关

### Q: 如何与Obsidian集成？
**A:** 
**方法1（推荐）：**
1. Obsidian → 设置 → 文件
2. 新文件默认位置 → Downloads/LearnKeeper

**方法2：**
定期手动移动文件到Obsidian vault

**方法3：**
使用自动同步工具（如FreeFileSync）

---

### Q: 支持AnythingLLM吗？
**A:** 
支持！文件是标准Markdown格式：
1. 保存文件
2. 在AnythingLLM中导入Downloads/LearnKeeper文件夹
3. 即可基于内容对话

---

### Q: 可以导出到Notion吗？
**A:** 
可以：
1. 文件已保存为Markdown
2. Notion → Import → Markdown
3. 选择LearnKeeper文件夹

---

## 🔒 隐私安全

### Q: 数据会上传到服务器吗？
**A:** 
**绝不！**
- 文件100%保存在你的电脑
- AI调用仅发送内容文本到硅基流动
- 不保存在任何云端

---

### Q: 需要注册账号吗？
**A:** 
**不需要！**
- 插件完全本地运行
- 无需登录
- 无需提供个人信息

---

### Q: 开源吗？可以审查代码吗？
**A:** 
**完全开源！**
- GitHub: https://github.com/PeterMeng88/learnkeeper
- MIT协议
- 欢迎审查和贡献代码

---

## 💰 成本相关

### Q: 完全免费吗？
**A:** 
- 插件：✅ 完全免费
- 基础保存：✅ 免费
- AI功能：💰 需要API密钥（有免费额度）

---

### Q: AI功能成本多少？
**A:** 
使用硅基流动：
- 新用户：免费额度约可保存1000次
- 后续：¥0.12/100万tokens
- 实际成本：约¥0.0001/次

对比：
- Notion AI: $10/月
- Mem.ai: $8/月
- LearnKeeper: ~¥1/年

---

## 🐛 故障排查

### Q: 点击保存没反应？
**A:** 
1. 右键插件图标 → 检查
2. 查看Console错误
3. 截图发到GitHub Issues

---

### Q: 提示"连接失败"？
**A:** 
- 后端未启动：启动 `python kb_backend.py`
- 端口被占用：重启后端
- 防火墙拦截：允许Python访问网络

---

### Q: 文件内容是乱码？
**A:** 
用支持UTF-8的编辑器打开：
- ✅ VSCode
- ✅ Obsidian
- ✅ Typora
- ❌ Windows记事本（可能乱码）

---

## 🚀 高级用法

### Q: 可以批量保存吗？
**A:** 
目前不支持，在路线图中。
临时方案：配合键盘脚本使用。

---

### Q: 可以自定义保存模板吗？
**A:** 
可以！修改 `backend/kb_backend.py` 中的markdown模板。

---

### Q: 如何备份数据？
**A:** 
文件在Downloads/LearnKeeper/，直接：
- 方法1：复制整个文件夹
- 方法2：用云盘同步（百度网盘、OneDrive等）
- 方法3：Git版本管理

---

## 🤝 贡献相关

### Q: 如何报告Bug？
**A:** 
https://github.com/PeterMeng88/learnkeeper/issues

提供：
- 浏览器版本
- 插件版本
- 错误截图
- 操作步骤

---

### Q: 如何建议新功能？
**A:** 
GitHub Issues 中打上 `enhancement` 标签

---

### Q: 可以参与开发吗？
**A:** 
当然！
1. Fork仓库
2. 创建分支
3. 提交PR

---

## 📞 联系方式

- GitHub Issues: https://github.com/PeterMeng88/learnkeeper/issues
- Twitter: @learnkeeper
- Email: learnkeeper.official@gmail.com

---

**找不到答案？**  
[提交新问题](https://github.com/PeterMeng88/learnkeeper/issues/new)
