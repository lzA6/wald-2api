from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Dict
import re
import requests


def getCompletionLLMEngine():
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://app.wald.ai/chat/1aafb80c-7ca1-41fb-9c15-07e82ff833b2",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    }
    url = "https://app.wald.ai/_next/static/chunks/pages/_app-f8a44b58964e7359.js"
    response = requests.get(url, headers=headers)
    text = response.text

    # 方法1: 先定位到整个对象，然后提取键值对
    pattern = r"Enums\.CompletionLLMEngine\s*=\s*\{([^}]+)\}"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1)
        # 提取所有的键值对
        pairs = re.findall(r'(\w+):\s*"([^"]+)"', content)
        result_dict = {key: value for key, value in pairs}
        return result_dict
    else:
        return False


def getImageGenerationEngine():
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://app.wald.ai/chat/1aafb80c-7ca1-41fb-9c15-07e82ff833b2",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    }
    url = "https://app.wald.ai/_next/static/chunks/pages/_app-f8a44b58964e7359.js"
    response = requests.get(url, headers=headers)
    text = response.text

    # 方法1: 先定位到整个对象，然后提取键值对
    pattern = r"Enums\.ImageGenerationEngine\s*=\s*\{([^}]+)\}"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1)
        # 提取所有的键值对
        pairs = re.findall(r'(\w+):\s*"([^"]+)"', content)
        result_dict = {key: value for key, value in pairs}
        return result_dict
    else:
        return False


def getMODEL_MAPPING():
    CompletionLLMEngine = getCompletionLLMEngine()
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://app.wald.ai/chat/1aafb80c-7ca1-41fb-9c15-07e82ff833b2",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    }
    url = "https://app.wald.ai/_next/static/chunks/1635-86c05d14cf03b50f.js"
    response = requests.get(url, headers=headers)
    js_code = response.text
    """更严格的匹配方案"""
    result = {}

    # 更精确的正则表达式
    pattern = r'\[r\.CompletionLLMEngine\.(\w+)\]:\s*\{(?:[^{}]|\{[^{}]*\})*?displayName:\s*["\']([^"\']+)["\']'

    matches = re.finditer(pattern, js_code, re.DOTALL)

    for match in matches:
        engine_name = match.group(1)
        display_name = match.group(2)
        result[display_name] = CompletionLLMEngine[engine_name]
    return result


def getIMAGE_MODEL_MAPPING():
    ImageGenerationEngine = getImageGenerationEngine()
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://app.wald.ai/chat/1aafb80c-7ca1-41fb-9c15-07e82ff833b2",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    }
    url = "https://app.wald.ai/_next/static/chunks/1635-86c05d14cf03b50f.js"
    response = requests.get(url, headers=headers)
    js_code = response.text
    """更严格的匹配方案"""
    result = {}

    # 更精确的正则表达式
    pattern = r'\[r\.ImageGenerationEngine\.(\w+)\]:\s*\{(?:[^{}]|\{[^{}]*\})*?displayName:\s*["\']([^"\']+)["\']'

    matches = re.finditer(pattern, js_code, re.DOTALL)

    for match in matches:
        engine_name = match.group(1)
        display_name = match.group(2)
        result[display_name] = ImageGenerationEngine[engine_name]
    return result


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "wald-2api"
    APP_VERSION: str = "1.1.0"
    DESCRIPTION: str = "一个将 app.wald.ai 转换为兼容 OpenAI 格式 API 的高性能代理。"

    API_MASTER_KEY: Optional[str] = None
    WOS_SESSION_COOKIE: Optional[str] = None

    API_REQUEST_TIMEOUT: int = 180
    NGINX_PORT: int = 8088

    # 模型别名到 Wald.ai 内部 llmEngine 名称的精确映射
    MODEL_MAPPING: Dict[str, str] = getMODEL_MAPPING()
    IMAGE_MODEL_MAPPING: Dict[str, str] = getIMAGE_MODEL_MAPPING()


settings = Settings()
