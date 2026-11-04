from hello_agents import HelloAgentsLLM

def test_hello_agents_llm():
  try:
    llmClient = HelloAgentsLLM()

    example_messages = [
      {"role": "system", "content": "You are a helpful assistant that writes Python code."},
      {"role": "user", "content": "写一个快速排序算法的 Python 实现"}
    ]

    print("LLM 思考结果:")
    result = llmClient.think(example_messages)
    if result:
      print("\n\n--- 思考结果 ---")
      print(result)
    else:
      print("LLM 没有生成任何内容")
  except Exception as e:
    print(f"运行示例失败: {e}")