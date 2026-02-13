import asyncio
from agents.base import Agent


class PolicyAgent(Agent):
    async def run(self):
        while True:
            await asyncio.sleep(2)
            await self.bus.publish({
                'type': 'command',
                'target': 'thermostat',
                'action': 'set',
                'value': 22
            })