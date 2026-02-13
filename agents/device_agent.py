from agents.base import Agent


class DeviceAgent(Agent):
    async def execute(self, command: dict):
        print(f"[{self.name}] Executing {command}")

    async def run(self):
        pass