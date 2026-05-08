import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv('DASHSCOPE_API_KEY')
base_url = os.getenv('ALI_BASE_URL')
model_name = os.getenv('ALI_MODE')
tavily_api_key = os.getenv('TAVILY_API_KEY')

# 创建model
model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url
)


# 获取体重工具方法
@tool
def get_weight() -> int:
    """
    获取体重返回一个整数值
    :return:
    """
    return 65


# 获取身高工具方法
@tool
def get_height() -> int:
    """
    获取身高返回是整数值
    :return:
    """
    return 175


agent = create_agent(
    model=model,
    tools=[get_weight, get_height],
    system_prompt="你是一个严格遵循ReAct框架智能体，必须按照【思考->行动->观察->再思考】的流程解决问题，且每轮只能思考并调用一个工具方法，不能重复调用工具方法，请勿重复调用工具方法，"
                  "请勿重复调用工具方法，请勿重复调用工具方法，禁止单次调用多个工具方法，并且告知你思考过程，工具调用的原因，按思考、行动、观察三个结构告知。"
)

for chunk in agent.stream(
        {"messages": [{"role": "user", "content": "请计算我的BMI指数"}]}
        , stream_mode="values"):
    latest_message = chunk.get("messages")[-1]
    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content)

    try:
        if latest_message.tool_calls:
            print(f'调用工具方法:{[tc["name"] for tc in latest_message.tool_calls]}')

    except Exception as e:
        print(e)




