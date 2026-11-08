import asyncio

from src.core.generator import generate
from src.core.server_manager import ServerManager, wait_server
from src.core.emotionAnalyzer import apply_emotion
from src.core.state import get_amadeus, get_world
from src.core.tick import tick_amadeus, state_to_text
import json
from datetime import datetime

SERVER_EXE = r"S:\llama-ai\llama.cpp\build\bin\Release\llama-server.exe"
MODEL_GGUF = r"S:\llama-ai\modelos\llama.gguf"

running = True
TICK_INTERVAL = 1

async def voice_loop(amadeus, world):
    server = ServerManager(SERVER_EXE, MODEL_GGUF)
    server.start()
    if not wait_server():
        print("[voz] servidor não subiu — corpo segue vivo, só a voz calou")
        server.stop()
        return
    try:
        while running:
            userMsg = await asyncio.to_thread(input, "> ")
            apply_emotion(userMsg, amadeus.affect)
            await generate(userMsg, amadeus)
    finally:
        server.stop()


async def main():
    amadeus = get_amadeus()
    world = get_world()

    goals_status = amadeus.get_status()["goals"]
    if goals_status["daily_generated"] is None and goals_status["active_goals"]:
        amadeus._goal_engine._last_daily_generation = datetime.now()
        
    amadeus.start()
    
    with open('log.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(amadeus.get_status(), indent=2, ensure_ascii=False, default=str))
        file.write("\n")
    try:
        await voice_loop(amadeus, world)
    finally:
        amadeus.stop()
        
if __name__ == "__main__":
    asyncio.run(main())