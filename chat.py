import asyncio

from src.core.generator import reply, initiate
from src.core.server_manager import ServerManager, wait_server
from src.utils.utils import save_status_to_log
from src.core.emotionAnalyzer import apply_emotion
from src.core.state import get_amadeus, get_world
from src.core.tick import state_to_text
from datetime import datetime

SERVER_EXE = r"S:\llama-ai\llama.cpp\build\bin\Release\llama-server.exe"
MODEL_GGUF = r"S:\llama-ai\modelos\llama.gguf"

running = True

async def voice_loop(amadeus, world):
    server = ServerManager(SERVER_EXE, MODEL_GGUF)
    server.start()
    if not await asyncio.to_thread(wait_server):
        print("[voz] servidor não subiu — corpo segue vivo, só a voz calou")
        return
    try:
        while running:
            userMsg = await asyncio.to_thread(input, "> ")
            amadeus.on_user_message(userMsg)
            apply_emotion(userMsg, amadeus.affect)
            #save_status_to_log(amadeus)
            await reply(userMsg, amadeus)
    finally:
        server.stop()


async def debug_loop(amadeus):
    while True:
        s = amadeus.get_status()["scheduler"]["last_ticks"]
        print(f"[debug] world={s['world']} energy={s['energy']} activity={s['activity']} plan={s['plan']} goal={s['goal']}")
        await asyncio.sleep(5 * 60)


async def main():
    amadeus = get_amadeus()
    world = get_world()

    amadeus.start()
    debug_task = asyncio.create_task(debug_loop(amadeus))
    try:
        await voice_loop(amadeus, world)
    finally:
        debug_task.cancel()
        amadeus.stop()
        
if __name__ == "__main__":
    asyncio.run(main())