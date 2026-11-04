from hello_agents.llm_client import HelloAgentsLLM
from hello_agents.tools.tools_manager import ToolsManager
from hello_agents.tools.search_web import search
from .re_act import ReActAgent

def test_re_act():
  llm = HelloAgentsLLM()
  tools_manager = ToolsManager()

  search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具"
  tools_manager.register_tool("search_web", search_desc, search)

  agent = ReActAgent(llm_client=llm, tools_manager=tools_manager)
  question = "苹果最新的手机是哪一款？主要的卖点是什么？"

  agent.run(question)