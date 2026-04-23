import yaml
import os

def get_rag_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../config/rag.yml")
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

# ... existing code ...

def get_redis_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../config/redis.yml")
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

model_config = get_rag_config()
redis_config = get_redis_config()

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print( os.path.join(script_dir, "../config/rag.yml"))
