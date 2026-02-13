# Smart Home Orchestrator


A multi-agent smart home automation system designed for **low latency**, **compressed state sharing**, and **deterministic coordination**.


## Features
- Async event-driven architecture
- Delta-compressed world state (msgpack)
- Modular agent-based design
- Easily extensible to MQTT / Matter / Home Assistant


## Run
```bash
pip install -r requirements.txt
python main.py