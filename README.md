# LearnKeeper

> 🧠 Your AI-powered learning companion

Save, organize, and chat with your knowledge. Local-first, AI-enhanced, open source.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/PeterMeng88/learnkeeper)](https://github.com/PeterMeng88/learnkeeper/stargazers)

---

## ✨ Features

- 🔖 **One-click Save** - Save web content with browser extension
- 🤖 **AI Summary** - Automatic extraction of key points and insights  
- 🏠 **Local Storage** - 100% privacy, files saved locally
- 💬 **Knowledge Chat** - Talk with your knowledge base using RAG
- 🔗 **Easy Integration** - Works with Obsidian & AnythingLLM
- 💰 **Low Cost** - ~$0.0001 per AI call

---

## 🚀 Quick Start

### Installation

#### 1. Download Extension

Go to [Releases](https://github.com/PeterMeng88/learnkeeper/releases) and download **`learnkeeper-extension-v0.1.2.zip`**

#### 2. Install Extension

1. Extract the zip file
2. Open Chrome: `chrome://extensions/`
3. Enable **"Developer mode"** (top right toggle)
4. Click **"Load unpacked"**
5. Select the extracted folder
6. Done! ✅

#### 3. Use It

1. Browse any webpage
2. Click the LearnKeeper icon
3. Add notes and tags (optional)
4. Click "Save"
5. Files saved to: `Downloads/LearnKeeper/`

#### 4. Setup Backend (Optional - for AI features)

**Not required for basic saving. Only needed for AI summary and key points extraction.**

**a. Install Python (if you don't have it)**
- Download: https://www.python.org/downloads/
- Version: 3.8+
- Check "Add to PATH" during installation

**b. Install dependencies**
``` 
cd backend 
pip install -r requirements.txt
```

**c. Get API Key**
1. Sign up: https://cloud.siliconflow.cn  
2. Get your API key (free credits available)  

**d. Configure**  
1. Rename `env-example.txt` to `.env`  
2. Open `.env` and add your API key:  

SILICONFLOWAPIKEY=sk-your-key-here  

**e. Start backend**
```
python kb_backend.py  
```

You should see: `✅ AI功能已启用`

**f. Keep it running**
- Don't close the terminal
- Now saving pages will include AI summaries  

---

## 📖 Usage

### Basic Saving
1. Click extension icon on any webpage
2. Add personal notes (optional)
3. Click "Save"
4. File saved to `Downloads/LearnKeeper/`

### With AI Enhancement
1. Start backend first (`python kb_backend.py`)
2. Save pages as usual
3. AI will automatically:
   - Generate summary
   - Extract key points
   - Suggest tags

### Integrate with Obsidian
**Method 1: Set Obsidian vault to Downloads folder**
1. Obsidian → Settings → Files
2. Set vault location: `Downloads/LearnKeeper`

**Method 2: Move files manually**
1. Files are in `Downloads/LearnKeeper/`
2. Copy to your Obsidian vault
3. Or set up auto-sync with tools

---

## 🛠️ Tech Stack

- **Frontend**: Chrome Extension (Manifest V3)
- **Backend**: Python FastAPI
- **AI**: SiliconFlow (Qwen 2.5-7B)
- **Storage**: Local Markdown files
- **Integration**: Obsidian, AnythingLLM

---

## 🗺️ Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] More AI models support
- [ ] Knowledge graph visualization
- [ ] Smart review system
- [ ] Team collaboration
- [ ] Browser sync

---

## 🤝 Contributing

Contributions welcome! 

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🌟 Support

If this project helps you, please give it a ⭐!

**Links:**
- [GitHub Issues](https://github.com/PeterMeng88/learnkeeper/issues)
- [Releases](https://github.com/PeterMeng88/learnkeeper/releases)
- [Twitter](https://twitter.com/learnkeeper)

---

## 📝 FAQ

**Q: Do I need to run the backend?**  
A: No. The extension works standalone. Backend is only for AI features.

**Q: Where are my files saved?**  
A: In your Downloads folder, under `LearnKeeper/` subfolder.

**Q: Can I change the save location?**  
A: Currently files go to Downloads. You can move them to Obsidian manually or set Obsidian to monitor that folder.

**Q: Is it free?**  
A: Yes. Extension is free. AI features use SiliconFlow which has free tier.

**Q: Does it work offline?**  
A: Extension works offline. AI features need internet.

---

**Built with ❤️ by LearnKeeper Team**

