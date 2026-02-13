import asyncio


class MessageBus:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def publish(self, message: dict):
        await self.queue.put(message)

    async def subscribe(self):
        return await self.queue.get()
        
