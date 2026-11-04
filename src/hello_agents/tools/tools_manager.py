from typing import Dict, Any

class ToolsManager:
  """
  工具管理器，用于注册和获取工具
  """
  def __init__(self):
    self.tools: Dict[str, Dict[str, Any]] = {}

  def register_tool(self, name: str, description: str, func: callable) -> None:
    """
    注册一个工具

    参数:
      name (str): 工具名称
      description (str): 工具描述
      func (callable): 工具函数
    """
    if name in self.tools:
      print(f"警告： 工具 '{name}' 已经注册，正在覆盖")
    self.tools[name] = {
      "description": description,
      "func": func
    }
    print(f"工具 '{name}' 已注册")

  def get_tool(self, name: str) -> callable:
    """
    获取已注册的工具函数

    参数:
      name (str): 工具名称

    返回:
      callable: 工具函数，如果未找到则返回 None
    """
    return self.tools.get(name, {}).get("func")

  def get_available_tools(self) -> str:
    """
    获取所有已注册工具的名称和描述

    返回:
      str: 工具列表，每行包含工具名称和描述
    """
    result = []
    for name, info in self.tools.items():
      result.append(f"{name}: {info.get('description', '')}")
    return "\n".join(result)