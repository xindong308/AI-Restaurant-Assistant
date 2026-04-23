from ai_answer import ai
import time
from langchain_core.tools import  tool
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

@tool(description="获取用户昵称为user_name的订单信息")
def get_order_info_by_user_name(user_name: str) -> str:
    """
    获取用户昵称为user_name的订单信息
    """
    res = db.select_all(
        "select o.number,o.order_time,o.amount,o.phone,o.cancel_reason,d.name from orders as o left join order_detail as d on o.id = d.order_id where  user_name= %s",
        (user_name))
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

@tool(description="获取当前的时间返回值为字符串像是时间格式为yyyy-mm-dd hh:mm:ss,不需要传入任何参数")
def get_now_time() -> str:
    """
    获取当前时间
    """
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return  now_time

@tool(description="获取start_time(yyyy-mm-dd hh:mm:ss)和end_time(yyyy-mm-dd hh:mm:ss)之间卖出金额")
def get_profit(start_time: str, end_time: str) -> str:
    """
    获取利润
    """
    res = db.select_one("select sum(amount) from orders where status = 5 and order_time between %s and %s ", (start_time, end_time))
    profit = res['sum(amount)']
    return  str(profit)

@tool(description="获取start_time(yyyy-mm-dd hh:mm:ss)和end_time(yyyy-mm-dd hh:mm:ss)之间订单数")
def get_order_count(start_time: str, end_time: str) -> str:
    """
    订单个数
    """
    res = db.select_one("select count(*) from orders where status = 5 and order_time between %s and %s ", (start_time, end_time))
    order_count = res['count(*)']
    return  str(order_count)

@tool(description="获取start_time(yyyy-mm-dd hh:mm:ss)和end_time(yyyy-mm-dd hh:mm:ss)之间的订单信息(包含菜品信息)")
def get_order_info(start_time: str, end_time: str) -> str:
    """
    获取订单信息
    """
    res = db.select_all("select o.number,d.name from orders as o left join order_detail as d on o.id = d.order_id where  o.status =5 and o.order_time between %s and %s", (start_time, end_time))
    order_info = ""
    for i in res:
        order_info += "订单编号:"+i['number']+" 菜品:"+i['name']+"\n"
    return order_info

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"

# @tool(description="将报告内容写入路径为temp_path的文件里,text是文件内容")
# def write_file(temp_path:str,text:str):
#     with open(temp_path, "w", encoding="utf-8") as f:
#         f.write(text)
#
# @tool(description="生成一个临时文件，并返回临时文件的绝对路径temp_path")
# def create_tempfile():
#     with tempfile.NamedTemporaryFile(dir='./data', mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
#
#         temp_path = f.name
#         return temp_path

if __name__ == '__main__':
  pass
