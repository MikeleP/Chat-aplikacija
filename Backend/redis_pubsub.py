import redis.asyncio as aioredis
import asyncio

class RedisPubSubManager:
    def __init__(self, url="redis://localhost:6379"):
        self.redis = aioredis.from_url(url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.channel_name = "chat"

    async def subscribe(self):
        await self.pubsub.subscribe(self.channel_name)

    async def publish(self, message: str):
        await self.redis.publish(self.channel_name, message)

    async def listen(self):
        async for message in self.pubsub.listen():
            if message and message["type"] == "message":
                yield message["data"]
