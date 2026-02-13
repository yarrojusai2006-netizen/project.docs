import asyncio
import os
import sys
from config import get_api_key
from core.messaging import MessageBus
from core.orchestrator import Orchestrator
from agents.sensor_agent import SensorAgent
from agents.policy_agent import PolicyAgent
from simulation.mock_sensors import (
    mock_temperature_sensor,
    mock_motion_sensor
)


async def main(api_key: str = None):
    # Use provided API key or get from environment
    if api_key is None:
        api_key = os.getenv('API_KEY', '')
    
    bus = MessageBus()
    orchestrator = Orchestrator(bus, api_key=api_key)

    agents = [
        SensorAgent("temp_sensor", bus, api_key=api_key),
        PolicyAgent("policy", bus, api_key=api_key)
    ]

    await asyncio.gather(
        orchestrator.run(),
        *[agent.run() for agent in agents],
        mock_temperature_sensor(bus),
        mock_motion_sensor(bus)
    )


if __name__ == "__main__":
    # Get API key from command line, .env file, environment, or user input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = get_api_key()  # Read from .env file first
        if not api_key:
            api_key = input("Enter your API key (or press Enter to skip): ").strip()
            api_key = api_key if api_key else None
    
    asyncio.run(main(api_key))






