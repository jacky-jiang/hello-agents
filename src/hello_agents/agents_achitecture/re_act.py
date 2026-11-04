import re
from hello_agents.llm_client import HelloAgentsLLM
from hello_agents.tools import tools_manager as ToolsManager, search_web as search

REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""

class ReActAgent:
  def __init__(self, llm_client: HelloAgentsLLM, tools_manager: ToolsManager, max_steps: int = 5):
    self.llm_client = llm_client
    self.tools_manager = tools_manager
    self.max_steps = max_steps
    self.history = []

  def run(self, question: str):
    self.history = []
    current_step = 0

    while current_step < self.max_steps:
      current_step += 1
      print(f"Step {current_step}:")

      tools_desc = self.tools_manager.get_available_tools()
      history_str = "\n".join(self.history)
      prompt = REACT_PROMPT_TEMPLATE.format(
        tools=tools_desc,
        question=question,
        history=history_str
      )
      messages = [{"role": "user", "content": prompt}]
      response_text = self.llm_client.think(messages=messages)
      if not response_text:
        print("No response from LLM.")
        break

      print(f"LLM Response: {response_text}")
      thought, action = self._parse_output(response_text)
      if thought:
        print(f"Thought: {thought}")
      if not action:
        print("警告：未找到有效的行动，流程终止。")
        break
      if action.startswith("Finish"):
        final_answer = self._parse_action_input(action)
        print("Finished with answer:", final_answer)
        return final_answer
      tool_name, tool_input = self._parse_action(action)
      if not tool_name or not tool_input:
        self.history.append("Observation:无效的Action格式，请检查");continue

      print(f"行动: {tool_name} 输入: {tool_input}")
      tool_function = self.tools_manager.get_tool(tool_name)
      observation = tool_function(tool_input) if tool_function else f"工具 {tool_name} 未找到"

      print(f"Observation: {observation}")
      self.history.append(f"Action: {action}")
      self.history.append(f"Observation: {observation}")

    print("Reached max steps without finishing.")
    return None

  def _parse_output(self, text: str):
    # Thought: 匹配到 Action: 或文本末尾
    thought_match = re.search(r"Thought:(.*?)(?=Action:|$)", text, re.DOTALL)

    # Action: 匹配到文本末尾
    action_match = re.search(r"Action:\s*(.*?)(?=$)", text, re.DOTALL)

    thought = thought_match.group(1).strip() if thought_match else ""
    action = action_match.group(1).strip() if action_match else ""
    return thought, action

  def _parse_action(self, action: str):
    match = re.match(r"(\w+)\[(.*)\]", action, re.DOTALL)
    return (match.group(1), match.group(2)) if match else (None, None)

  def _parse_action_input(self, action_input: str):
    match = re.match(r"\w+\[(.*)\]", action_input, re.DOTALL)
    return match.group(1) if match else None

  