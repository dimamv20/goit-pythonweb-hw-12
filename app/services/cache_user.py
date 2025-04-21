from services.redis_service import redis_client
import json
from app.schemas import UserRead

CACHE_EXPIRE_SECONDS = 300 

def cache_user(user: UserRead):
    key = f"user:{user.id}"
    redis_client.setex(key, CACHE_EXPIRE_SECONDS, user.json())

def get_cached_user(user_id: int):
    key = f"user:{user_id}"
    user_data = redis_client.get(key)
    if user_data:
        return UserRead.parse_raw(user_data)
    return None

def clear_cached_user(user_id: int):
    redis_client.delete(f"user:{user_id}")
