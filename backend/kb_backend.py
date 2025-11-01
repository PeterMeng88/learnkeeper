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

load_dotenv()  # ← 必须有这行

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AnythingLLM 配置
ANYTHINGLLM_API_URL = "http://localhost:3001/api"  # AnythingLLM 地址
ANYTHINGLLM_API_KEY = os.getenv('ANYTHINGLLM_API_KEY', '')  # ← 替换成你的 API Key
ANYTHINGLLM_WORKSPACE = os.getenv('ANYTHINGLLM_WORKSPACE', '')  # ← 替换成你的工作空间名称
USE_ANYTHINGLLM = True  # 是否启用自动上传

# 配置硅基流动
USE_AI = False
client = None

try:
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv('SILICONFLOW_API_KEY', ''),  # ← 你的硅基流动 API Key
        base_url="https://api.siliconflow.cn/v1"
    )
    
    # 启动时测试连接
    print("正在测试AI连接...")
    test_response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": "测试"}],
        max_tokens=10
    )
    
    USE_AI = True
    print("✅ AI功能已启用（硅基流动 - Qwen2.5-7B）")
    
except ImportError:
    print("⚠️ 未安装 openai 模块，AI功能未启用")
    print("   安装命令: pip install openai")
    
except Exception as e:
    print(f"⚠️ AI功能启动失败: {e}")
    print("   请检查:")
    print("   1. API Key 是否正确")
    print("   2. 网络是否能访问 api.siliconflow.cn")
    print("   3. 硅基流动账户是否有余额")

class ContentData(BaseModel):
    title: str
    url: str
    content: str
    notes: str = ""
    tags: list = []
    vault_path: str
    metadata: dict = {}

def safe_filename(title):
    """生成安全的文件名"""
    filename = re.sub(r'[\\/*?:"<>|]', "", title)
    return filename[:50]

async def process_with_ai(content, title):
    """使用AI增强处理内容"""
    if not USE_AI or not client:
        return {
            "summary": "AI功能未启用",
            "key_points": [],
            "suggested_tags": []
        }
    
    # 内容太短不处理
    if len(content) < 100:
        return {
            "summary": "内容较短，未生成摘要",
            "key_points": [],
            "suggested_tags": []
        }
    
    try:
        # 限制内容长度，节省成本
        content_preview = content[:2000]
        
        prompt = f"""请分析以下内容，并严格按照JSON格式返回结果（不要有任何其他文字）：

{{
  "summary": "用一句话总结核心内容（50字内）",
  "key_points": ["知识点1", "知识点2", "知识点3", "知识点4"],
  "suggested_tags": ["标签1", "标签2", "标签3", "标签4", "标签5"]
}}

标题：{title}

内容：
{content_preview}

要求：
1. summary要准确完整
2. key_points提取最重要的4个
3. suggested_tags要全面，包括：主题、领域、技术、概念等
"""
        
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "你是内容分析助手。只返回JSON格式，不要有其他解释文字。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        print(f"AI返回原文: {result_text[:200]}")
        
        # 提取JSON部分
        start = result_text.find('{')
        end = result_text.rfind('}') + 1
        
        if start != -1 and end > start:
            json_str = result_text[start:end]
            result = json.loads(json_str)
            print(f"AI解析结果: {result}")
            return result
        else:
            print("❌ 未找到JSON格式")
            return {
                "summary": "AI返回格式错误",
                "key_points": [],
                "suggested_tags": []
            }
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"   原始返回: {result_text}")
        return {
            "summary": "AI返回格式错误",
            "key_points": [],
            "suggested_tags": []
        }
    
    except Exception as e:
        print(f"❌ AI处理失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "summary": f"AI处理失败: {str(e)}",
            "key_points": [],
            "suggested_tags": []
        }

async def upload_to_anythingllm(filepath, filename):
    """上传文件到 AnythingLLM"""
    if not USE_ANYTHINGLLM:
        print("⚠️ AnythingLLM同步未启用")
        return {"success": False, "message": "AnythingLLM未启用"}
    
    if ANYTHINGLLM_API_KEY == "your-anythingllm-api-key-here":
        print("⚠️ 请先配置 AnythingLLM API Key")
        return {"success": False, "message": "API Key未配置"}
    
    try:
        print(f"📤 开始上传到 AnythingLLM: {filename}")
        
        headers = {
            'Authorization': f'Bearer {ANYTHINGLLM_API_KEY}',
            'accept': 'application/json'
        }
        
        # 1. 上传文档
        upload_url = f"{ANYTHINGLLM_API_URL}/v1/document/upload"
        
        with open(filepath, 'rb') as f:
            files = {
                'file': (filename, f, 'text/markdown')
            }
            
            print(f"   请求URL: {upload_url}")
            upload_response = requests.post(
                upload_url,
                files=files,
                headers=headers,
                timeout=30
            )
        
        print(f"   上传响应状态: {upload_response.status_code}")
        print(f"   上传响应内容: {upload_response.text[:500]}")
        
        if upload_response.status_code != 200:
            return {
                "success": False, 
                "message": f"上传失败: {upload_response.status_code} - {upload_response.text}"
            }
        
        upload_result = upload_response.json()
        
        # 2. 获取文档位置
        doc_location = None
        if 'location' in upload_result:
            doc_location = upload_result['location']
        elif 'document' in upload_result and 'location' in upload_result['document']:
            doc_location = upload_result['document']['location']
        elif 'documents' in upload_result and len(upload_result['documents']) > 0:
            doc_location = upload_result['documents'][0].get('location')
        
        print(f"   文档位置: {doc_location}")
        
        if not doc_location:
            print("⚠️ 未获取到文档位置，尝试直接返回成功")
            return {"success": True, "message": "文档已上传（未获取位置）"}
        
        # 3. 添加到工作空间
        workspace_url = f"{ANYTHINGLLM_API_URL}/v1/workspace/{ANYTHINGLLM_WORKSPACE}/update-embeddings"
        
        embed_payload = {
            "adds": [doc_location]
        }
        
        print(f"   添加到工作空间: {workspace_url}")
        print(f"   Payload: {embed_payload}")
        
        embed_response = requests.post(
            workspace_url,
            json=embed_payload,
            headers=headers,
            timeout=60
        )
        
        print(f"   索引响应状态: {embed_response.status_code}")
        print(f"   索引响应内容: {embed_response.text[:500]}")
        
        if embed_response.status_code == 200:
            print(f"✅ 已同步到 AnythingLLM 并索引")
            return {"success": True, "message": "已同步到AnythingLLM"}
        else:
            return {
                "success": False, 
                "message": f"索引失败: {embed_response.status_code} - {embed_response.text}"
            }
        
    except requests.exceptions.Timeout:
        print(f"❌ AnythingLLM同步超时")
        return {"success": False, "message": "请求超时"}
    
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到 AnythingLLM")
        return {"success": False, "message": "连接失败，请确认 AnythingLLM 正在运行"}
    
    except Exception as e:
        print(f"❌ AnythingLLM同步失败: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": str(e)}

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
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_filename(data.title)}_{timestamp}.md"
        filepath = os.path.join(data.vault_path, filename)
        
        # 生成增强的Markdown
        markdown = f"""---
title: {data.title}
url: {data.url}
tags: {', '.join(all_tags)}
source: {data.metadata.get('source', '网页')}
type: {data.metadata.get('type', '文章')}
created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

# {data.title}

## 🔗 原文链接
{data.url}

## 📝 AI摘要
{ai_result.get('summary', '暂无摘要')}

## 💡 关键知识点
"""
        
        # 添加知识点
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

---
> 📌 来源：{data.metadata.get('source', '网页')}  
> ⏰ 保存时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> 🤖 AI处理：{'是' if USE_AI else '否'}
"""
        
        # 确保目录存在
        os.makedirs(data.vault_path, exist_ok=True)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"✅ 文件已保存: {filename}")
        
        # 自动上传到 AnythingLLM
        anythingllm_result = await upload_to_anythingllm(filepath, filename)
        
        print(f"{'='*50}\n")
        
        return {
            "success": True,
            "message": "保存成功",
            "file": filename,
            "ai_enhanced": USE_AI,
            "suggested_tags": ai_result.get('suggested_tags', []),
            "anythingllm_synced": anythingllm_result.get('success', False),
            "anythingllm_message": anythingllm_result.get('message', '')
        }
    
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "message": f"保存失败: {str(e)}"
        }

@app.get("/")
async def root():
    return {
        "status": "知识库API运行中",
        "ai_enabled": USE_AI,
        "ai_provider": "硅基流动 (Qwen2.5-7B)" if USE_AI else "未配置",
        "anythingllm_enabled": USE_ANYTHINGLLM and ANYTHINGLLM_API_KEY != "your-anythingllm-api-key-here"
    }

@app.get("/test-ai")
async def test_ai():
    """测试AI功能"""
    if not USE_AI or not client:
        return {
            "error": "AI未启用",
            "message": "请检查API Key配置和网络连接"
        }
    
    try:
        # 使用更长的测试文本
        test_content = """
        人工智能（Artificial Intelligence，AI）是计算机科学的一个重要分支。
        它致力于创建能够执行通常需要人类智能的任务的系统。
        这包括学习、推理、问题解决、感知和语言理解等多种能力。
        人工智能技术已经广泛应用于各个领域，包括医疗诊断、自动驾驶、
        语音识别、图像识别、自然语言处理等。随着深度学习和神经网络技术的发展，
        人工智能正在快速改变我们的生活方式和工作方式。
        """
        
        result = await process_with_ai(test_content, "人工智能简介")
        
        return {
            "success": True,
            "result": result,
            "message": "AI功能正常"
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "message": "AI测试失败"
        }

@app.get("/test-anythingllm")
async def test_anythingllm():
    """测试 AnythingLLM 连接"""
    if not USE_ANYTHINGLLM:
        return {"error": "AnythingLLM 未启用"}
    
    if ANYTHINGLLM_API_KEY == "your-anythingllm-api-key-here":
        return {"error": "请先配置 AnythingLLM API Key"}
    
    try:
        headers = {
            'Authorization': f'Bearer {ANYTHINGLLM_API_KEY}',
            'accept': 'application/json'
        }
        
        # 测试连接：获取工作空间列表
        test_url = f"{ANYTHINGLLM_API_URL}/v1/workspaces"
        
        response = requests.get(test_url, headers=headers, timeout=10)
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "message": "连接成功" if response.status_code == 200 else "连接失败"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "测试失败"
        }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 知识库后端服务启动中...")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
