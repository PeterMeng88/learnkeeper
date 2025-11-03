# LearnKeeper

> 🧠 你的AI学习助手

保存、整理网页内容，用AI对话学习。本地优先，隐私安全，开源免费。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/PeterMeng88/learnkeeper)](https://github.com/PeterMeng88/learnkeeper/stargazers)

[English](README.md) · [简体中文](README.zh-CN.md)

---

## ✨ 特性

- 🔖 **一键保存** - 浏览器插件保存网页内容
- 🤖 **AI摘要** - 自动提取关键知识点和摘要
- 🏠 **本地存储** - 100%隐私保护，文件保存在本地
- 💬 **知识对话** - 基于知识库的AI问答
- 🔗 **无缝集成** - 支持Obsidian和AnythingLLM
- 💰 **成本极低** - 每次AI调用约¥0.0001

### 📺 演示

![Demo](docs/demo.gif)

*一键保存，AI自动增强*

---

## 🚀 快速开始

### 安装

#### 1. 下载插件

前往 [Releases](https://github.com/PeterMeng88/learnkeeper/releases) 下载最新版 **`learnkeeper-extension-v0.1.3.zip`**

#### 2. 安装到Chrome

1. 解压zip文件
2. 打开Chrome：`chrome://extensions/`
3. 开启右上角 **"开发者模式"**
4. 点击 **"加载已解压的扩展程序"**
5. 选择解压后的文件夹
6. 完成！✅

#### 3. 使用

1. 访问任意网页
2. 点击LearnKeeper图标
3. 添加笔记和标签（可选）
4. 点击"保存"
5. 文件保存在：`下载/LearnKeeper/`

#### 4. 启用AI功能（可选）

**不启动后端也能正常保存，只是没有AI自动摘要**

**a. 安装Python（如果还没有）**
- 下载：https://www.python.org/downloads/
- 版本：3.8+
- 安装时勾选"添加到PATH"

**b. 安装依赖**
```
cd backend
pip install -r requirements.txt
```


**c. 获取API密钥**
1. 注册：https://cloud.siliconflow.cn
2. 获取API密钥（有免费额度）

**d. 配置**
1. 将 `env-example.txt` 重命名为 `.env`
2. 编辑 `.env`，填入你的密钥：
SILICONFLOWAPIKEY=sk-你的密钥


**e. 启动后端**
```
python kb_backend.py
```


看到 `✅ AI功能已启用` 表示成功

**f. 保持运行**
- 不要关闭终端窗口
- 现在保存网页会自动生成AI摘要

---

## 📖 使用方法

### 基础保存
1. 点击任意网页上的插件图标
2. 添加个人笔记（可选）
3. 点击"保存"
4. 文件保存到 `下载/LearnKeeper/`

### AI增强模式
1. 先启动后端（`python kb_backend.py`）
2. 正常保存网页
3. AI会自动：
   - 生成内容摘要
   - 提取关键知识点
   - 建议相关标签

### 与Obsidian集成

**方法1：设置Obsidian仓库**
1. Obsidian → 设置 → 文件
2. 仓库位置设为：`下载/LearnKeeper`

**方法2：手动移动**
1. 文件在 `下载/LearnKeeper/`
2. 复制到你的Obsidian仓库
3. 或使用自动同步工具

---

## 🛠️ 技术栈

- **前端**：Chrome扩展（Manifest V3）
- **后端**：Python FastAPI
- **AI**：硅基流动（通义千问2.5-7B）
- **存储**：本地Markdown文件
- **集成**：Obsidian、AnythingLLM

---

## 🗺️ 开发路线

- [ ] 移动端应用（iOS/Android）
- [ ] 支持更多AI模型
- [ ] 知识图谱可视化
- [ ] 智能复习系统
- [ ] 团队协作功能
- [ ] 浏览器同步

---

## 🤝 贡献

欢迎贡献代码！

1. Fork本仓库
2. 创建特性分支
3. 提交你的修改
4. 推送到分支
5. 开启Pull Request

---

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE)

---

## 🌟 支持

如果这个项目对你有帮助，请给个⭐！

**相关链接：**
- [GitHub Issues](https://github.com/PeterMeng88/learnkeeper/issues)
- [版本发布](https://github.com/PeterMeng88/learnkeeper/releases)
- [Twitter](https://twitter.com/learnkeeper)

---

## 📝 常见问题

**Q: 必须运行后端吗？**  
A: 不需要。插件独立工作。后端仅用于AI功能。

**Q: 文件保存在哪里？**  
A: 在下载文件夹的 `LearnKeeper/` 子文件夹中。

**Q: 可以修改保存位置吗？**  
A: 目前保存到下载文件夹。可以手动移动或设置Obsidian监听该文件夹。

**Q: 完全免费吗？**  
A: 是的。插件免费。AI功能使用硅基流动的免费额度。

**Q: 离线能用吗？**  
A: 插件离线可用。AI功能需要联网。

---

**用❤️构建 by LearnKeeper团队**
