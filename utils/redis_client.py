import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def blacklist_token(token: str, expires_in: int):
    redis_client.setex(
        f"blacklist:{token}",
        expires_in,
        "true"
    )

def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") > 0    