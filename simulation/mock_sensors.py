import asyncio
import random
from core.compression import StateCompressor

async def mock_temperature_sensor(bus, name="mock_temp"):
    while True:
        delta = {
            'temperature': round(18 + random.random() * 6, 2)
        }
        await bus.publish({
            'type': 'state_delta',
            'source': name,
            'payload': StateCompressor.compress(delta)
        })
        await asyncio.sleep(1.5)


async def mock_motion_sensor(bus, name="mock_motion"):
    while True:
        delta = {
            'motion': random.choice([True, False])
        }
        await bus.publish({
            'type': 'state_delta',
            'source': name,
            'payload': StateCompressor.compress(delta)
        })
        await asyncio.sleep(3)