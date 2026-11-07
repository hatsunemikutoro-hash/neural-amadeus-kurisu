import asyncio

from src.core.generator import generate
from src.core.server_manager import ServerManager, wait_server
from src.core.emotionAnalyzer import apply_emotion
from src.core.state import get_amadeus, get_world
from src.core.tick import tick_amadeus

SERVER_EXE = r"S:\llama-ai\llama.cpp\build\bin\Release\llama-server.exe"
MODEL_GGUF = r"S:\llama-ai\modelos\llama.gguf"

running = True
TICK_INTERVAL = 15

async def tick_loop(world, amadeus):
    while running:
        tick_amadeus(world, amadeus)
        await asyncio.sleep(TICK_INTERVAL)


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
            world.user_spoke()
            apply_emotion(userMsg, amadeus.affect)
            await generate(userMsg, amadeus)
    finally:
        server.stop()


async def main():
    amadeus = get_amadeus()
    world = get_world()

    voice_task = asyncio.create_task(voice_loop(amadeus, world))
    try:
        await tick_loop(world, amadeus)
    finally:
        voice_task.cancel()
        try:
            await voice_task
        except asyncio.CancelledError:
            pass