import json
import redis

class RedisCache:
    def __init__(self, redis_config):
        self.__client = redis.Redis(
            host=redis_config['host'],
            port=redis_config['port'],
            decode_responses=True,
            username=redis_config['username'],
            password=redis_config['password']
        )

    def cache_key(self, key:str, payload:dict):
        return self.__client.set(key, json.dumps(payload,default=str),ex=3600)

    def retrieve_from_cache(self, key:str):
        response = self.__client.get(key)
        print("redis response:", response)
        if not response:
            return None
        return json.loads(self.__client.get(key))
