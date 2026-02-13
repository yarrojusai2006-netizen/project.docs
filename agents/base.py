import asyncio


class Agent:
    def __init__(self, name, bus, api_key: str = None):
        self.name = name
        self.bus = bus
        self.api_key = api_key

    async def run(self):
        raise NotImplementedError