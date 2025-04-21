import redis
from dotenv import dotenv_values

config = dotenv_values(".env")

redis_client = redis.Redis(
    host=config["REDIS_HOST"],
    port=int(config["REDIS_PORT"]),
    db=0,
    decode_responses=True
)
