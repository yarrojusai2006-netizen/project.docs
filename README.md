# Smart Home Orchestrator

A multi-agent smart home automation system designed for **low latency**, **compressed state sharing**, and **deterministic coordination**. Built with Python's `asyncio` for highly responsive smart home control across sensors, policies, and devices.

## Overview

The Smart Home Orchestrator is an event-driven architecture that manages smart home devices through independent, asynchronous agents communicating via a central message bus. It supports real-time sensor monitoring, policy-based decision making, and device control all in a unified, scalable framework.

### Key Design Principles
- **Async-First**: Non-blocking I/O for responsive event handling
- **Extensible**: Modular agent architecture supports custom sensors, policies, and devices
- **Efficient**: Delta-compressed state transmission using msgpack
- **Deterministic**: Centralized orchestration ensures consistent state across all agents

---

## Features

✨ **Core Capabilities**
- ✅ Async event-driven architecture with asyncio
- ✅ Delta-compressed world state sharing (msgpack)
- ✅ Modular agent-based design (Sensor, Policy, Device agents)
- ✅ Real-time message bus for inter-agent communication
- ✅ Mock sensor simulation for testing
- ✅ Extensible to MQTT, Matter, Home Assistant

📦 **Architecture Components**
- **Orchestrator**: Central coordinator managing world state and message routing
- **Agents**: Independent entities (Sensor, Policy, Device) running concurrently
- **Message Bus**: Pub/sub system for agent-to-agent communication
- **World State**: Shared, compressed state tracking across all agents
- **Mock Sensors**: Simulation layer for development and testing

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yarrojusai2006-netizen/project.git
   cd project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key** (optional)
   Create a `.env` file in the project root:
   ```
   API_KEY=your_api_key_here
   ```
   Or provide at runtime:
   ```bash
   python main.py <your_api_key>
   ```

---

## Project Structure

```
project/
├── main.py                    # Application entry point
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys, etc.)
│
├── core/                      # Core system components
│   ├── __init__.py
│   ├── orchestrator.py        # Central orchestrator managing world state
│   ├── messaging.py           # Message bus for inter-agent communication
│   ├── state.py               # World state management
│   └── compression.py         # State delta compression (msgpack)
│
├── agents/                    # Agent implementations
│   ├── __init__.py
│   ├── base.py                # Base Agent class
│   ├── sensor_agent.py        # Sensor monitoring and reporting
│   ├── policy_agent.py        # Policy logic and decision making
│   └── device_agent.py        # Device control and actuation
│
├── devices/                   # Smart device simulations
│   ├── __init__.py
│   ├── light.py               # Smart light control
│   └── thermostat.py          # Smart thermostat control
│
└── simulation/                # Mock components for testing
    ├── mock_sensors.py        # Simulated sensor data (temperature, motion)
    └── __pycache__/
```

---

## Quick Start

### Run the Orchestrator

```bash
python main.py
```

With an API key:
```bash
python main.py your_api_key_here
```

The system will:
1. Start the central Orchestrator
2. Launch Sensor and Policy Agents
3. Simulate sensor readings (temperature, motion)
4. Process events through the message bus
5. Update world state based on sensor and policy inputs

### Expected Output
```
[SensorAgent] Publishing temperature: 22.5°C
[PolicyAgent] Evaluating policies...
[Orchestrator] State updated: {temp: 22.5, motion: false}
```

---

## Usage Guide

### Creating a Custom Sensor Agent

```python
from agents.base import Agent
from core.messaging import MessageBus

class CustomSensorAgent(Agent):
    async def run(self):
        while True:
            # Read sensor data
            sensor_value = await self.read_sensor()
            
            # Publish to message bus
            await self.bus.publish({
                'type': 'sensor_reading',
                'sensor': self.name,
                'value': sensor_value
            })
            
            await asyncio.sleep(1)
    
    async def read_sensor(self):
        # Your sensor logic here
        return 42
```

### Creating a Custom Policy Agent

```python
from agents.policy_agent import PolicyAgent

class CustomPolicyAgent(PolicyAgent):
    async def evaluate_policies(self, state):
        # state contains current world state
        if state.get('temperature', 0) > 25:
            # Too hot, cool down
            await self.bus.publish({
                'type': 'command',
                'action': 'cool',
                'intensity': 0.8
            })
```

### Publishing Custom Messages

```python
from core.messaging import MessageBus

bus = MessageBus()

# Publish a state delta
await bus.publish({
    'type': 'state_delta',
    'payload': {'room_temp': 22.5, 'light_on': True}
})

# Subscribe to messages
message = await bus.subscribe()
print(f"Received: {message}")
```

---

## Configuration

### Environment Variables (.env)

```bash
# OpenAI or compatible API key
API_KEY=sk-...

# Optional: Custom settings
LOG_LEVEL=INFO
SENSOR_INTERVAL=5  # seconds
STATE_SYNC_INTERVAL=10  # seconds
```

### Programmatic Configuration

Modify `config.py` to change behavior:

```python
def load_config():
    """Load configuration from .env file"""
    config = {}
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                # Parse config...
```

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Smart Home Orchestrator                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Central Message Bus                    │   │
│  │    (Pub/Sub event routing, msgpack compress)     │   │
│  └──────────────────────────────────────────────────┘   │
│           ↑              ↑              ↑                │
│           │              │              │                │
│  ┌────────┴──┐  ┌────────┴──┐  ┌────────┴──┐           │
│  │  Sensor   │  │   Policy  │  │  Device   │           │
│  │  Agent    │  │   Agent   │  │  Agent    │           │
│  └───────────┘  └───────────┘  └───────────┘           │
│           │              │              │                │
│           └──────────────┼──────────────┘                │
│                          │                               │
│              ┌───────────▼──────────┐                    │
│              │  World State         │                    │
│              │  (Compressed Deltas) │                    │
│              └──────────────────────┘                    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │    Simulation Layer (Mock Sensors)              │    │
│  │  - Temperature sensor                           │    │
│  │  - Motion detector                              │    │
│  └────────────────────────────────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Examples

### Example 1: Temperature-Based Thermostat Control

```python
import asyncio
from core.orchestrator import Orchestrator
from agents.sensor_agent import SensorAgent
from core.messaging import MessageBus

async def thermostat_example():
    bus = MessageBus()
    orchestrator = Orchestrator(bus)
    
    # Temperature sensor publishes readings
    # Policy agent reads temperatures and triggers thermostat
    # Device agent adjusts cooling/heating
    
    await asyncio.gather(
        orchestrator.run(),
    )

# Run example
# asyncio.run(thermostat_example())
```

### Example 2: Motion-Triggered Lighting

```python
# When motion is detected, turn on lights
# When motion stops for 2 minutes, turn off lights

# Implement in PolicyAgent:
async def evaluate_policies(self, state):
    motion = state.get('motion', False)
    light_on = state.get('light_on', False)
    
    if motion and not light_on:
        await self.bus.publish({
            'type': 'command',
            'device': 'light',
            'action': 'turn_on',
            'brightness': 100
        })
```

---

## API Reference

### Orchestrator

```python
orchestrator = Orchestrator(bus, api_key=None)
await orchestrator.run()          # Main event loop
orchestrator.world                # Current world state (WorldState object)
```

### Message Bus

```python
bus = MessageBus()
await bus.publish(message)        # Publish a message
msg = await bus.subscribe()       # Subscribe to next message
```

### Agent Base Class

```python
agent = Agent(name, bus, api_key=None)
await agent.run()                 # Main agent loop
agent.name                        # Agent identifier
agent.bus                         # Reference to message bus
```

### State Compression

```python
from core.compression import StateCompressor

compressed = StateCompressor.compress(state_delta)
original = StateCompressor.decompress(compressed)
```

---

## Dependencies

- **asyncio**: Built-in async I/O framework
- **msgpack**: Efficient binary serialization for state compression

See `requirements.txt` for exact versions.

---

## Extending the System

### Adding a New Agent Type

1. Create a new file in `agents/`:
   ```python
   from agents.base import Agent
   
   class MyCustomAgent(Agent):
       async def run(self):
           # Your custom logic
           pass
   ```

2. Register in `main.py`:
   ```python
   agents = [
       MyCustomAgent("my_agent", bus, api_key=api_key),
       # ... other agents
   ]
   ```

### Integrating with Home Assistant

Extend the message bus to publish MQTT messages:
```python
async def handle_message(self, msg):
    # Publish to Home Assistant via MQTT
    mqtt_client.publish(f"homeassistant/{msg['device']}", msg['action'])
```

### Integrating with Matter

Implement a Matter endpoint that listens to the message bus and translates commands to Matter protocol actions.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not found | Ensure `.env` file exists with `API_KEY=...` or pass as argument |
| Agents not communicating | Check message bus is initialized and shared across all agents |
| State not updating | Verify state delta format: `{'type': 'state_delta', 'payload': {...}}` |
| High CPU usage | Reduce `asyncio.sleep()` intervals in agent loops |

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## License

MIT License - see LICENSE file for details.

---

## Contact & Support

- **GitHub**: [yarrojusai2006-netizen/project](https://github.com/yarrojusai2006-netizen/project)
- **Issues**: [GitHub Issues](https://github.com/yarrojusai2006-netizen/project/issues)

---

**Last Updated**: February 2026  
**Version**: 1.0.0
