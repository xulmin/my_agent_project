from typing import Callable, Union
from utils.prompt_loader import load_system_prompt, load_report_prompt
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger


@wrap_tool_call # 工具执行的监控
def monitor_tool(
        request: ToolCallRequest,# 请求的数据封装
        handler: Callable[[ToolCallRequest], Union[ToolMessage, Command]], # 执行的函数本身
) -> Union[ToolMessage, Command]:
    """
    监控工具
    :param request:
    :param handler:
    :return:
    """
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        # 如果是报告生成场景，则将报告生成场景的标志设置为True
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e


@before_model  # 在模型执行前输出日志
def log_before_model(
        state: AgentState,          # 整个Agent智能体中的状态记录
        runtime: Runtime,           # 记录了整个执行过程中的上下文信息
):
    """
    请用用模型前监控
    :param state:
    :param runtime:
    :return:
    """
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")

    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None


@dynamic_prompt   # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):     # 动态切换提示词
    """
    动态提示词
    :param request:
    :return:
    """
    is_report = request.runtime.context.get("report", False)
    if is_report:               # 是报告生成场景，返回报告生成提示词内容
        return load_report_prompt()

    return load_system_prompt()