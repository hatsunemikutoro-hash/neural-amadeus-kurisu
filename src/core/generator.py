import sys
import httpx
from openai import AsyncOpenAI
from rich.console import Console
import random

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

# geracao indireta de respostas, pega apenas o historico recente
async def initiate(reason: str, amadeus) -> str:
    status = state_to_text(amadeus)
    history = [
        message
        for message in memory.get_messages()
        if message.get("role") != "system"
    ][-4:]

    messages = [
        {
            "role": "system",
            "content": f"{system_prompt}\n\n[Estado atual]\n{status}",
        },
        *history,
        {
            "role": "user",
            "content": f"[instrução interna] {reason}. Fale espontaneamente.",
        },
    ]

    chunks: list[str] = []
    console.print("[bold cyan]Kurisu > [/bold cyan]", end="")

    try:
        response = await client.chat.completions.create(
            model="qwen-local",
            messages=messages,
            stream=True,
            temperature=0.9,
            presence_penalty=0.3,
            frequency_penalty=0.3,
            max_tokens=256,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": False}
            },
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

    full_response = "".join(chunks).strip()
    if full_response:
        memory.add_msg("assistant", full_response)

    return full_response
    
# interacao direta com o usuario, pega TODO  o historico
async def reply(msg: str, amadeus) -> str:
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
            extra_body={
                            "chat_template_kwargs": {"enable_thinking": False},
                            "seed": random.randint(0, 2**31 - 1),
                        },
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