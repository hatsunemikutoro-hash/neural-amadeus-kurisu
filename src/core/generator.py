import sys
import httpx
from openai import AsyncOpenAI
from rich.console import Console

from src.core.memory import MemoryManager
from src.core.tick import state_to_text

client = AsyncOpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-no-key-required",
    timeout=httpx.Timeout(60.0, connect=5.0),
)

console = Console()

with open("agent_kurisu.txt", "r", encoding="utf-8") as prompt:
    system_prompt = prompt.read()

memory = MemoryManager(system_prompt)

async def generate(msg: str, amadeus) -> str:
    memory.add_msg("user", msg)

    status = state_to_text(amadeus)
    msgs = memory.get_messages()
    msgs[0] = {
        "role": "system",
        "content": f"{system_prompt}\n\n[Estado atual]\n{status}",
    }
    
    chunks: list[str] = []

    console.print("[bold cyan]Kurisu > [/bold cyan]", end="")

    try:
        response = await client.chat.completions.create(
            model="qwen-local",
            messages=msgs,
            stream=True,
            temperature=0.9,
            presence_penalty=0.3,
            frequency_penalty=0.3,
            max_tokens=256,
        )

        async for chunk in response:
            if not chunk.choices:
                continue
            text = chunk.choices[0].delta.content
            if text:
                chunks.append(text)
                sys.stdout.write(text)
                sys.stdout.flush()

    except Exception as e:
        console.print(f"\n[red][erro: {e}][/red]")

    finally:
        console.print()

    full_response = "".join(chunks)
    if full_response:
        memory.add_msg("assistant", full_response)
    return full_response