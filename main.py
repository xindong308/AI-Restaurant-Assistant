from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from Agent.admin_agent import ai as admin_ai
from Agent.user_agent import ai as user_ai
from ai_answer import ai
from model.input   import Query
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/user/ai")
async def get_user_response(input: Query):
    query = input.query
    user_id = input.id
    answer = await user_ai.get_answer(query,user_id)
    res = answer["messages"][-1]
    # 保存对话
    user_ai.save_new_session(user_id, query, res)
    return {"message": res}

@app.post("/admin/ai")
async def get_admin_response(input: Query):
    query = input.query
    emply_id = input.id
    answer = await admin_ai.get_answer(query,emply_id)
    res = answer["messages"][-1]
    # 保存 对话
    await ai.save_new_session(emply_id=emply_id,query=query, answer=reply)
    return {"message": res}
# @app.get("/user/profit")
# async def test():
#     file_path =  "./config/img.png"
#     return FileResponse( path=file_path,
#                          filename="img.png",
#                          media_type="image/png",
#                         )