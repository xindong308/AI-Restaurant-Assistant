from hmac import new
from utils.logger_handler import logger
from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from Agent.tools.user_agent_tools import rag_summarize,get_order_info_by_order_number,get_order_info_by_userid,get_now_time
from Agent.tools.middleware import monitor_tool,prompt_switch
from utils.config_handler import model_config
import asyncio
from utils.prompt_util import user_prompt

from utils.redis_client import redis_set_session,redis_get_session, redis_delete,get_redis_length
class Agent:
    def __init__(self):
        self.agent = create_agent(
            model=ChatTongyi(model=model_config["chat_model_name"]),
            system_prompt=user_prompt,
            tools=[rag_summarize,get_order_info_by_userid,get_now_time,get_order_info_by_order_number,],
            middleware=[monitor_tool]
         )

    # 获取消息
    async def get_answer(self,query:str=None,user_id:int=None):
        context =  {"user_id": user_id}
        history_list = []
        new_list = []
        # res = await redis_get_session("test")
        res = await redis_get_session(str(user_id)) #用时把测试用例注销，使用这个
        if res:
            for i in res:
                history_list.append({"role":i[0], "content": i[1]})
        history_list.extend([
            {"role": "system", "content": "结合上述历史对话历史对话回答问题"},
            {"role": "user", "content": query}
        ])
        new_list.extend(history_list)
        input_dict = {"messages": new_list}
        res = self.agent.invoke(input_dict,context= context)
        return res

    # 存入新的消息
    async def save_new_session(self,user_id:int= None, query:str=None, answer:str=None):
        """
        保存新的会话
        :param user_id:
        :return:
        """
        prefix  = "user"
        key = f"{prefix}_{user_id}"
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
    async def main():
        # if i.role == "ai"
        res = await agent.get_answer("我的所有历史订单",user_id=1)
        res = res["messages"][-1]
        # reply = [i for i in res_l ]
        # # for i in res_l:
        # #     print(type(i).__name__ + ":" + i.content)
        # print(type(reply[-1]).__name__,reply[-1].content)
        print(res.content)
    asyncio.run(main())
