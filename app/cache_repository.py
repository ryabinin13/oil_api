import json
from redis import Redis


class CacheRepository():
    def __init__(self, redis_connection: Redis):
        self.redis = redis_connection

    def get_data(self, key):

        cache_key = f"{key}"
        return self.redis.get(cache_key)

    
    def set_date(self, dates, key):
        self.redis.set(key, json.dumps(dates, default=str))


    def set_spr(self, all_data, key):

        data_to_serialize = [item.as_dict() for item in all_data]
        self.redis.set(key, json.dumps(data_to_serialize, default=str))