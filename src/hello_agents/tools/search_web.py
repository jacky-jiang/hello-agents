import os
from serpapi import Client

def search(query: str) -> str:
  """
  使用 SerpApiClient 搜索网页

  参数:
    query (str): 搜索查询字符串

  返回:
    str: 搜索结果的字符串表示
  """
  print(f"Searching for: {query}")
  try:
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
      raise ValueError("SERPAPI_API_KEY 环境变量未设置")
    params = {
      "q": query,
      "engine": "google",
      "api_key": api_key,
    }
    client = Client(api_key = api_key)
    results = client.search(params)

    # 智能解析：优先寻找最直接的答案
    if "answer_box_list" in results:
        return "\n".join(results["answer_box_list"])
    if "answer_box" in results and "answer" in results["answer_box"]:
        return results["answer_box"]["answer"]
    if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
        return results["knowledge_graph"]["description"]
    if "organic_results" in results and results["organic_results"]:
      # 如果没有直接答案，则返回前三个有机结果的摘要
      snippets = [
          f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
          for i, res in enumerate(results["organic_results"][:3])
      ]
      return "\n\n".join(snippets)
    
    return f"对不起，没有找到关于 '{query}' 的信息。"
  except Exception as e:
    print(f"搜索失败: {e}")
    return ""