from typing import Callable
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
import logging

from utils.prompt_util import admin_prompt,report_prompt


@wrap_tool_call
def monitor_tool(
        # 请求的数据封装
        request: ToolCallRequest,
        # 执行的函数本身
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"{request.tool_call['name']}调用")
    # logger.info(f"用户id为:{request.runtime.context['user_id']}")
    res = handler(request)
    try:
        res = handler(request)
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True
    except Exception as e:
        logger.error(f"{request.tool_call['name']}调用失败{e}")
        raise e
    return  res

@dynamic_prompt
def prompt_switch(
        request: ModelRequest
) -> str:
    """
    动态生成prompt
    """
    is_report = request.runtime.context.get("report", False)
    if is_report:
        logger.info("报告切换成功")
        return report_prompt
    return admin_prompt

