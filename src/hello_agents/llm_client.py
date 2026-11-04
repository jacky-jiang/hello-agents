import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()  # 加载 .env 文件中的环境变量

class HelloAgentsLLM:
  """
  定制 LLM 客户端
  用于调用任何兼容 OpenAI 接口的服务，并默认使用流式响应
  """
  def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
    """
    初始化 HelloAgentsLLM 实例

    参数:
      model (str): 模型 ID，默认为环境变量中的 LLM_MODEL_ID
      apiKey (str): API Key，默认为环境变量中的 LLM_API_KEY
      baseUrl (str): 基础 URL，默认为环境变量中的 LLM_BASE_URL
      timeout (int): 请求超时时间，单位为秒
    """
    self.model = model or os.getenv("LLM_MODEL_ID")
    self.apiKey = apiKey or os.getenv("LLM_API_KEY")
    self.baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
    self.timeout = timeout or 60  # 默认超时时间为 60 秒

    if not all([self.model, self.apiKey, self.baseUrl]):
      raise ValueError("模型 ID、API Key 和基础 URL 都不能为空")

    self.client = OpenAI(api_key=self.apiKey, base_url=self.baseUrl, timeout=self.timeout)

  def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
    """
    调用 LLM 进行思考

    参数:
      messages (List[Dict[str, str]]): 消息列表，每条消息包含 "role" 和 "content"
      temperature (float): 生成文本的温度，默认为 0

    返回:
      str: LLM 生成的文本
    """
    print(f"正在调用 {self.model} 模型，温度为 {temperature}")
    try:
      response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        temperature=temperature,
        stream=True,
      )
      # 处理流式响应
      collected_content = []
      for chunk in response:
        if not chunk.choices:
          continue
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        collected_content.append(content)
      print()  # 换行，确保输出整洁
      return "".join(collected_content)
    except Exception as e:
      print(f"调用 LLM 失败: {e}")
      return None