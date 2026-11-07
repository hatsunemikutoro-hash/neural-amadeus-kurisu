import time, statistics
from piper import PiperVoice

voice = PiperVoice.load("dii_pt-BR.onnx", config_path="dii_pt-BR.onnx.json")
texto = "Eu sou a Makise Kurisu, neurocientista. Não me chame de assistente, eu tenho nome."

# warmup
list(voice.synthesize(texto))

tempos, ttfа = [], []
for _ in range(10):
    t0 = time.perf_counter()
    t_first = None
    dur = 0
    for chunk in voice.synthesize(texto):
        if t_first is None:
            t_first = time.perf_counter() - t0
        dur += len(chunk.audio_int16_bytes) / 2 / voice.config.sample_rate
    tempos.append(time.perf_counter() - t0)
    ttfа.append(t_first)

print(f"total médio : {statistics.mean(tempos)*1000:.0f} ms")
print(f"TTFA médio  : {statistics.mean(ttfа)*1000:.0f} ms")
print(f"RTF         : {statistics.mean(tempos)/dur:.2f}x")