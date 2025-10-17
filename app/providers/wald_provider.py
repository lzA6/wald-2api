import httpx
import json
import time
import logging
import uuid
import re
from typing import Dict, Any, AsyncGenerator, List

from fastapi.responses import StreamingResponse, JSONResponse

from app.core.config import settings
from app.providers.base_provider import BaseProvider
from app.utils.sse_utils import create_sse_data, create_chat_completion_chunk, DONE_CHUNK

logger = logging.getLogger(__name__)

class WaldAIProvider(BaseProvider):
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=settings.API_REQUEST_TIMEOUT)
        self.api_url = "https://app.wald.ai/api/chat"

    async def chat_completion(self, request_data: Dict[str, Any]) -> StreamingResponse:
        
        async def stream_generator() -> AsyncGenerator[bytes, None]:
            request_id = f"chatcmpl-{uuid.uuid4()}"
            model_requested = request_data.get("model", "gpt-3.5-turbo")
            
            try:
                payload = self._prepare_payload(request_data)
                headers = self._prepare_headers()

                async with self.client.stream("POST", self.api_url, headers=headers, json=payload, follow_redirects=True) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        
                        try:
                            if line.startswith('0:"'):
                                json_string_to_parse = line[2:]
                                actual_content = json.loads(json_string_to_parse)
                                
                                # [最终修正] 使用正则表达式彻底清除内部思考步骤
                                if isinstance(actual_content, str) and "<<<Workflow" in actual_content:
                                    # 使用 re.sub 清除从 '<<<' 开始的所有内容
                                    clean_content = re.sub(r'<<<Workflow.*', '', actual_content, flags=re.DOTALL)
                                    logger.info(f"已过滤内部思考步骤，原始长度: {len(actual_content)}, 清理后长度: {len(clean_content)}")
                                    
                                    if clean_content.strip():
                                        chunk = create_chat_completion_chunk(request_id, model_requested, clean_content)
                                        yield create_sse_data(chunk)
                                    continue

                                chunk = create_chat_completion_chunk(request_id, model_requested, actual_content)
                                yield create_sse_data(chunk)

                        except json.JSONDecodeError:
                            logger.warning(f"无法解析SSE JSON内容: {line}")
                            continue
                        except Exception as e:
                            logger.warning(f"处理SSE数据块时出错: {line}, 错误: {e}")
                            continue
                
                final_chunk = create_chat_completion_chunk(request_id, model_requested, "", "stop")
                yield create_sse_data(final_chunk)
                yield DONE_CHUNK

            except httpx.HTTPStatusError as e:
                # [最终修正] 修复 ResponseNotRead 错误
                await e.response.aread() # 在访问 .text 之前必须读取响应体
                logger.error(f"上游服务器错误: {e.response.status_code} - {e.response.text}", exc_info=True)
                error_message = f"上游服务器错误: {e.response.status_code}. 响应: {e.response.text}"
                error_chunk = create_chat_completion_chunk(request_id, model_requested, error_message, "stop")
                yield create_sse_data(error_chunk)
                yield DONE_CHUNK
            except Exception as e:
                logger.error(f"处理流时发生未知错误: {e}", exc_info=True)
                error_message = f"内部服务器错误: {str(e)}"
                error_chunk = create_chat_completion_chunk(request_id, model_requested, error_message, "stop")
                yield create_sse_data(error_chunk)
                yield DONE_CHUNK

        return StreamingResponse(stream_generator(), media_type="text/event-stream")

    def _prepare_headers(self) -> Dict[str, str]:
        if not settings.WOS_SESSION_COOKIE:
            raise ValueError("WOS_SESSION_COOKIE 未在 .env 文件中配置。")
        
        return {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json",
            "Origin": "https://app.wald.ai",
            "Referer": "https://app.wald.ai/chat",
            "Cookie": f"wos-session={settings.WOS_SESSION_COOKIE}"
        }

    def _prepare_payload(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        openai_messages = request_data.get("messages", [])
        model_requested = request_data.get("model", "gpt-3.5-turbo")
        llm_engine = settings.MODEL_MAPPING.get(model_requested, "GPTo3")

        chat_id = str(uuid.uuid4())
        wald_messages: List[Dict[str, Any]] = []

        for i, msg in enumerate(openai_messages):
            content = msg.get("content", "")
            wald_messages.append({
                "id": str(uuid.uuid4()),
                "role": msg.get("role"),
                "chatId": chat_id,
                "parentMessageId": wald_messages[i-1]["id"] if i > 0 else None,
                "content": content,
                "sanitizedContent": content,
                "createdAt": f"{time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())}.{int(time.time() * 1000) % 1000:03d}Z",
                "obfuscationSize": 0,
                "obfuscationMap": "{}",
                "obfuscationCategories": "{}",
                "sanitizeEngine": "GPT4",
                "llmEngine": None,
                "persona": None,
                "assistantMode": None,
                "tokenLimit": None,
                "isStreaming": None,
                "engineSwitchReason": None,
                "sanitizationInterrupted": False,
                "sanitizationFailed": False,
                "completionFailed": None,
                "completionInterrupted": None,
                "sanitizeLatency_ms": 0,
                "thinkingDisabled": None,
                "thinkingDisabledReason": None,
                "customAssistantName": None,
                "customAssistantId": None,
                "sanitizedContentTuned": None,
                "sanitizationSkipped": False,
                "associatedDocIds": []
            })

        return {
            "prompt": "",
            "webSearchEnabled": True,
            "completionMessageId": str(uuid.uuid4()),
            "obfuscationMap": {},
            "llmEngine": llm_engine,
            "messages": wald_messages,
            "docs": [],
            "persona": "DEFAULT",
            "mode": "REGULAR",
            "chat": {"id": chat_id},
            "encryptedContent": {"encryptedData": "", "nonce": ""},
            "encryptedSanitizedContent": {"encryptedData": "", "nonce": ""},
            "obfuscationSize": 0,
            "encryptedObfuscationMap": {"encryptedData": "", "nonce": ""},
            "logKeyEncryptedPromptContent": {"encryptedData": "", "nonce": ""},
            "logKeyEncryptedPromptObfuscationMap": {"encryptedData": "", "nonce": ""},
            "logPublicKey": "bae2372c817be5a89e9a9c65547acbfcc1e2cba34c731b03e592e46eafb7b87f",
            "savePrompt": True,
            "isIncognitoMode": False,
            "fileDocumentIds": [],
        }

    async def get_models(self) -> JSONResponse:
        model_data = {
            "object": "list",
            "data": [
                {"id": name, "object": "model", "created": int(time.time()), "owned_by": "lzA6"}
                for name in settings.MODEL_MAPPING.keys()
            ]
        }
        return JSONResponse(content=model_data)
