import logging
from utils.logger_handler import logger
from ai_answer import ai
import time
from langchain.tools import tool, ToolRuntime
from utils.mysql_hander import db

import tempfile
import os


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    """
    获取答案
    """
    answer = ai.get_answer(query)
    return  answer

@tool(description="获取当前的时间返回值为字符串像是时间格式为yyyy-mm-dd hh:mm:ss,不需要传入任何参数")
def get_now_time() -> str:
    """
    获取当前时间
    """
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return  now_time

@tool(description="获取当前用户的所有订单信息从")
def get_order_info_by_userid(runtime: ToolRuntime) -> str:
    """
    获取订单信息
    """
    user_id = runtime.context["user_id"]
    res = db.select_all("select o.number,o.order_time,o.amount,o.phone,o.cancel_reason,d.name from orders as o left join order_detail as d on o.id = d.order_id where  user_id= %s", (user_id))
    order_list_info = ""
    for i in res:
        order_list_info += (
                "订单编号:" + i['number'] +
                " 订单时间:" + i['order_time'].strftime("%Y-%m-%d %H:%M:%S") +
                " 金额:" + str(i['amount']) +
                " 手机号:" + i['phone'] +
                " 取消原因:" + i['cancel_reason'] +
                " 菜品:" + i['name'] + "\n"
        )
        return order_list_info

@tool(description="根据订单编号order_number获取对应订单的详细信息 ")
def get_order_info_by_order_number(order_number: str) -> str:
    """
    获取订单信息
    """
    res = db.select_one("select o.number,o.order_time,o.amount,o.phone,o.cancel_reason,d.name from orders as o left join order_detail as d on o.id = d.order_id where  o.number= %s", (order_number))
    order_info = ""
    for i in res:
        order_info += (
                "订单编号:" + i['number'] +
                " 订单时间:" + i['order_time'].strftime("%Y-%m-%d %H:%M:%S") +
                " 金额:" + str(i['amount']) +
                " 手机号:" + i['phone'] +
                " 取消原因:" + i['cancel_reason'] +
                " 菜品:" + i['name'] + "\n"
        )
        return order_info


if __name__ == '__main__':
  pass
