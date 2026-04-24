from hmac import new
from utils.logger_handler import logger
from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from Agent.tools.admin_agent_tools import rag_summarize,get_profit,get_now_time,get_order_info,get_order_count,fill_context_for_report,get_order_info_by_user_name
from Agent.tools.middleware import monitor_tool,prompt_switch
from utils.config_handler import model_config
import asyncio
from utils.prompt_util import admin_prompt

from utils.redis_client import redis_set_session,redis_get_session, redis_delete,get_redis_length
class Agent:
    def __init__(self):
        self.agent = create_agent(
            model=ChatTongyi(model=model_config["chat_model_name"]),
            system_prompt=admin_prompt,
            tools=[rag_summarize,get_order_info_by_user_name,get_profit,get_now_time,get_order_info,get_order_count,fill_context_for_report],
            middleware=[monitor_tool,prompt_switch]
         )


    # 获取消息
    async def get_answer(self,query:str=None,emp_id:int=None):
        context  ={"report": False,
                   "emp_id": emp_id,
                   }
        history_list = []
        new_list = []
        # res = await redis_get_session("test")
        res = await redis_get_session(str(emp_id)) #用时把测试用例注销，使用这个
        if res:
            for i in res:
                history_list.append({"role":i[0], "content": i[1]})
        history_list.extend([
            {"role": "system", "content": "结合上述历史对话历史对话回答问题"},
            {"role": "user", "content": query}
        ])
        new_list.extend(history_list)
        input_dict = {"messages": new_list}
        res = self.agent.invoke(input_dict,context=  context)
        return res

    # 存入新的消息
    async def save_new_session(self,emply_id:int= None, query:str=None, answer:str=None):
        """
        保存新的会话
        :param user_id:
        :return:
        """
        prefix  = "emply"
        key = f"{prefix}_{emply_id}"
        try:
            len =await get_redis_length(key)
            if len >= 6:
                await redis_delete(key)
                await redis_delete(key)
            await redis_set_session(key, ("user", query))  # 测试用例
            await redis_set_session(key, ("ai", answer))  # 测试用例
        except Exception as e:
            logger.error(f"保存会话失败{e}")

ai = Agent()

if __name__ == '__main__':
    agent = Agent()
    # input_dict = {"messages": [{"role": "user", "content": "今天什么菜卖的最多"}]}
    # res = agent.agent.invoke(input_dict)
    # print(res)
    # print("*"*100)
    # res_l = res["messages"]
    # for i in res_l:
    #     print(type(i).__name__+":"+i.content)


    async def main():
        # if i.role == "ai"
        res = await agent.get_answer("查询用户昵称为：神 的订单")
        res_l = res["messages"]
        reply = [i for i in res_l ]
        # for i in res_l:
        #     print(type(i).__name__ + ":" + i.content)
        print(type(reply[-1]).__name__,reply[-1].content)
    asyncio.run(main())
