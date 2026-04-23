import redis.asyncio as redis
from utils.config_handler import redis_config
import json
import asyncio
redis_client = redis.Redis(host=redis_config['REDIS_HOST'],
              port=redis_config['REDIS_PORT'],
              db=redis_config['REDIS_DB'],
              decode_responses= True #作用：将返回的二进制数据转为字符串
              )

tuple01 = ("humain","你是谁")

# 存储redis-string结构json数据
async def redis_set_json(key, value, expire=60 * 60 * 24 * 7):
    # 将value转为json字符串再存储，避免存储时出现乱码，如中文字符等，
    # 如：{"name": "张三", "age": 18}
    try:
        if isinstance(value, (dict, list, tuple)):
            # ensure_ascii=False是中文乱码的解决方法
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.set(key, value, ex=expire)
        return True
    except Exception as e:
        print(f"设置缓存失败{e}")
        return False

# 获取redis-string结构json数据
async def redis_get_json(key):
    try:
        value = await redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"获取缓存失败{e}")
        return None

# 设置redis-list结构session对话缓存
async def redis_set_session(key, value, expire=60 * 60 * 24 * 7):
    """
    设置session对话缓存
    :param key:
    :param value:
    :param expire:
    :return:
    """
    value = json.dumps(value, ensure_ascii=False)
    try:
        await redis_client.rpush(key, value)
        await redis_client.expire(key, expire)
        return True
    except Exception as e:
        print(f"设置缓存失败{e}")
        return False

# 获取redis-list结构session对话缓存
async def redis_get_session(key):
    """
    获取session对话缓存
    :param key:
    :return:
    """
    try:
        raw_list = await redis_client.lrange(key, 0, -1)  # 获取全部元素
        if not raw_list:
            return []

        # 对每个 JSON 字符串反序列化，并转为 tuple
        tuple_list = [tuple(json.loads(item)) for item in raw_list]
        return tuple_list
    except Exception as e:
        print(f"获取缓存失败{e}")
        return None
# 删除redis-list结构session对话缓存
async def redis_delete(key):
    """
    删除缓存
    :param key:
    :return:
    """
    try:
        await redis_client.lpop(key)
        return True
    except Exception as e:
        print(f"删除缓存失败{e}")
        return False
# 获取数组长度
async def get_redis_length(key):
    """
    获取缓存长度
    :param key:
    :return:
    """
    try:
        return await redis_client.llen(key)
    except Exception as e:
        print(f"获取缓存长度失败{e}")
        return None
if __name__ == '__main__':
    # 存储列表元组
    async def main():
        # 存储列表元组
        # await redis_set_session("test", tuple01)
        mm = await redis_get_session("test")
        print(type(mm),mm)
        print("*"*20)
        for i in mm:
            print(type(i),i)
            print(i[1])

        # await redis_delete("test")
        print(await get_redis_length("test"))
    asyncio.run(main())
