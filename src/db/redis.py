import redis.asyncio as aioredis
from src.config import config

JTI_EXPIRY = 3600

token_blocklist = aioredis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) == 1 