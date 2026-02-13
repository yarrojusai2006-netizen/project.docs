import asyncio
import random
from agents.base import Agent
from core.compression import StateCompressor


class SensorAgent(Agent):
    async def run(self):
        while True:
            temperature = round(20 + random.random() * 5, 2)
            delta = {'temperature': temperature}
            payload = StateCompressor.compress(delta)
            await self.bus.publish({
                'type': 'state_delta',
                'source': self.name,
                'payload': payload
            })
            await asyncio.sleep(1)