import asyncio
from core.state import WorldState
from core.compression import StateCompressor


class Orchestrator:

    def __init__(self, bus, api_key: str = None):
        self.bus = bus
        self.world = WorldState()
        self.api_key = api_key

    async def run(self):
        while True:
            msg = await self.bus.subscribe()
            await self.handle_message(msg)

    async def handle_message(self, msg: dict):
        if msg['type'] == 'state_delta':
            delta = StateCompressor.decompress(msg['payload'])
            for k, v in delta.items():
                self.world.update(k, v)

        elif msg['type'] == 'command':
            print(f"Executing command: {msg}")
