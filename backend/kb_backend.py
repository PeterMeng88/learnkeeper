from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import re
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AnythingLLM 配置
ANYTHINGLLM_API_URL = "http://localhost:3001/api"
ANYTHINGLLM_API_KEY = os.getenv('ANYTHINGLLM_API_KEY', '')
ANYTHINGLLM_WORKSPACE = os.getenv('ANYTHINGLLM_WORKSPACE', '')
USE_ANYTHINGLLM = False  # 改为False，不使用AnythingLLM

# 配置硅基流动
USE_AI = False
client = None

try:
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv('SILICONFLOW_API_KEY', ''),
        base_url="https://api.siliconflow.cn/v1"
    )
    
    print("正在测试AI连接...")
    test_response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": "测试"}],
        max_tokens=10
    )
    
    USE_AI = True
    print("✅ AI功能已启用（硅基流动 - Qwen2.5-7B）")
    
except ImportError:
    print("⚠️ 未安装 openai 模块")
    
except Exception as e:
    print(f"⚠️ AI功能启动失败: {e}")

class ContentData(BaseModel):
    title: str
    url: str
    content: str
    notes: str = ""
    tags: list = []
    vault_path: str = ""  # 改为可选，默认空
    metadata: dict = {}

def safe_filename(title):
    filename = re.sub(r'[\\/*?:"<>|]', "", title)
    return filename[:50]

async def process_with_ai(content, title):
    if not USE_AI or not client:
        return {
            "summary": "AI功能未启用",
            "key_points": [],
            "suggested_tags": []
        }
    
    if len(content) < 100:
        return {
            "summary": "内容较短",
            "key_points": [],
            "suggested_tags": []
        }
    
    try:
        content_preview = content[:2000]
        
        prompt = f"""请分析以下内容，返回JSON：

{{
  "summary": "一句话总结（50字内）",
  "key_points": ["知识点1", "知识点2", "知识点3", "知识点4"],
  "suggested_tags": ["标签1", "标签2", "标签3", "标签4", "标签5"]
}}

标题：{title}
内容：{content_preview}
"""
        
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {"role": "system", "content": "返回JSON格式"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        print(f"AI返回: {result_text[:200]}")
        
        start = result_text.find('{')
        end = result_text.rfind('}') + 1
        
        if start != -1 and end > start:
            json_str = result_text[start:end]
            result = json.loads(json_str)
            print(f"AI解析结果: {result}")
            return result
        else:
            return {"summary": "解析失败", "key_points": [], "suggested_tags": []}
    
    except Exception as e:
        print(f"❌ AI处理失败: {e}")
        return {"summary": "AI处理失败", "key_points": [], "suggested_tags": []}

@app.post("/api/save-content")
async def save_content(data: ContentData):
    try:
        print(f"\n{'='*50}")
        print(f"📥 收到保存请求: {data.title}")
        print(f"📊 内容长度: {len(data.content)} 字符")
        
        # AI增强处理
        ai_result = await process_with_ai(data.content, data.title)
        
        # 合并标签
        all_tags = list(set(data.tags + ai_result.get('suggested_tags', [])))
        
        # 仅在有路径时保存文件
        if data.vault_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_filename(data.title)}_{timestamp}.md"
            filepath = os.path.join(data.vault_path, filename)
            
            markdown = f"""---
title: {data.title}
url: {data.url}
tags: {', '.join(all_tags)}
created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

# {data.title}

## 🔗 原文链接
{data.url}

## 📝 AI摘要
{ai_result.get('summary', '暂无摘要')}

## 💡 关键知识点
"""
            
            key_points = ai_result.get('key_points', [])
            if key_points:
                for i, point in enumerate(key_points, 1):
                    markdown += f"{i}. {point}\n"
            else:
                markdown += "暂无提取\n"
            
            markdown += f"""

## ✍️ 个人笔记
{data.notes if data.notes else '暂无笔记'}

## 📄 原文内容
{data.content[:5000]}{'...' if len(data.content) > 5000 else ''}
"""
            
            os.makedirs(data.vault_path, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            print(f"✅ 文件已保存: {filename}")
        else:
            print("⚠️ 未提供路径，仅返回AI结果")
            filename = "not_saved"
        
        print(f"{'='*50}\n")
        
        return {
            "success": True,
            "message": "处理成功",
            "summary": ai_result.get('summary', ''),
            "key_points": ai_result.get('key_points', []),
            "suggested_tags": ai_result.get('suggested_tags', []),
            "ai_enhanced": USE_AI
        }
    
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "message": f"处理失败: {str(e)}"
        }

@app.get("/")
async def root():
    return {
        "status": "知识库API运行中",
        "ai_enabled": USE_AI,
        "ai_provider": "硅基流动 (Qwen2.5-7B)" if USE_AI else "未配置"
    }

@app.get("/test-ai")
async def test_ai():
    if not USE_AI or not client:
        return {"error": "AI未启用"}
    
    try:
        test_content = "人工智能是计算机科学的分支，致力于创建能执行人类智能任务的系统，包括学习、推理等。"
        result = await process_with_ai(test_content, "AI测试")
        return {"success": True, "result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 知识库后端服务启动中...")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
