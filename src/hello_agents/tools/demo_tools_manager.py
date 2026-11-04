from .tools_manager import ToolsManager
from .search_web import search

def demo_tools_manager():
  print("运行工具管理器示例：")
  tools_manager = ToolsManager()
  description = '一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具'
  tools_manager.register_tool("search_web", description, search)

  print("已注册的工具如下：")
  print(tools_manager.get_available_tools())

  print("调用 search_web 工具，搜索【英伟达最新的GPU型号是什么】的结果：")
  tool_name = "search_web"
  tool_input = "英伟达最新的GPU型号是什么"
  tool_func = tools_manager.get_tool(tool_name)
  if tool_func:
    observation = tool_func(tool_input)
    print("观察到的结果：")
    print(observation)
  else:
    print(f"工具 '{tool_name}' 未找到")