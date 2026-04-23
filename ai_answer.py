from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import DashScopeEmbeddings
from elasticsearch import Elasticsearch
from langchain_core.output_parsers import StrOutputParser
from utils.config_handler import model_config
# es = Elasticsearch(
#     ["http://192.168.100.128:9200"],  # ES 地址
#     verify_certs=False  # 本地测试关闭证书验证
# )
# chat_model = ChatTongyi(model="qwen3-max")
# embedding_model = DashScopeEmbeddings(model="text-embedding-v4")
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
#         ("user", "用户提问：{input}")
#     ]
# )

class  AIAnswer:
    def __init__(self):
        self.es = Elasticsearch(
    ["http://192.168.100.128:9200"],  # ES 地址
    verify_certs=False  # 本地测试关闭证书验证
)
        self.chat_model = ChatTongyi(model=model_config["chat_model_name"])
        self.embedding_model = DashScopeEmbeddings(model=model_config["embedding_model_name"])
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是幸福餐饮的客服小助手 "),
            ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
            ("user", "用户提问：{input}")
        ])

    def get_similar_docs(self, query: str) -> dict:
        """
        获取与输入文本最相似的文档
        """
        vector_query = self.embedding_model.embed_query(query)
        content  = ""
        couny = 1
        body = {
            "size": 5,
            "query": {
                "function_score": {
                    "query": {"match_all": {}},
                    "functions": [
                        # 1. 给 dish_summary 超大权重，确保排第一
                        {
                            "filter": {"term": {"doc_type": "summary"}},
                            "weight": 10000
                        },
                        # 2. 向量打分（ES 8.14.0 支持）
                        {
                            "script_score": {
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                                    "params": {"query_vector": vector_query}
                                }
                            }
                        }
                    ],
                    "boost_mode": "sum",
                    "score_mode": "sum"
                }
            },
            "_source": ["content"]
        }
        response = self.es.search(
            index="rag_shenming",
            body=body
        )
        for hit in response["hits"]["hits"]:
            content +="["+"参考资料"+str(couny)+":"+ hit["_source"]["content"]+"]"+"\n"
            couny += 1

        dict_context = {"context": content,
                        "input":query}
        return dict_context

    def get_answer(self, query: str) -> str:
        """
        获取答案
        """
        dict_context = self.get_similar_docs(query)
        chain = self.prompt | self.chat_model | StrOutputParser()
        res = chain.invoke(dict_context)
        return res

ai = AIAnswer()

if __name__ == '__main__':
   ai = AIAnswer()
   print(ai.get_answer("今天是几号啦"))
