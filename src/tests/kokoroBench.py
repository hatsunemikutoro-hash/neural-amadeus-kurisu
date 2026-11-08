import time
import sherpa_onnx
import numpy as np

PASTA = "S:\\Vscode\\amadeus-mk-II\\kokoro-int8-multi-lang-v1_1" 

config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=f"{PASTA}/model.onnx",
            voices=f"{PASTA}/voices.bin",
            tokens=f"{PASTA}/tokens.txt",
            data_dir=f"{PASTA}/espeak-ng-data",
            lexicon=f"{PASTA}/lexicon-us-en.txt,{PASTA}/lexicon-zh.txt",
        ),
        num_threads=4,
        provider="cpu",
    ),
)

tts = sherpa_onnx.OfflineTts(config)

# Texto em japonês (se colocar português, o áudio vai sair bugado/engolido)
texto = "I am Makise Kurisu, a neuroscientist. Do not call me an assistant, I have a name."
voice_id = 0 # ID da jf_alpha no v1.1 (se não for, testa do 0 ao 10)

t0 = time.perf_counter()
audio = tts.generate(texto, sid=voice_id, speed=1.0)
t1 = time.perf_counter()

dur = len(audio.samples) / audio.sample_rate
rtf = (t1 - t0) / dur

print(f"Tempo: {t1-t0:.2f}s | Áudio: {dur:.2f}s | RTF: {rtf:.2f}x")

# Salva pra você ouvir
import wave
with wave.open("teste_jp.wav", "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(audio.sample_rate)
    f.writeframes(np.array(audio.samples, dtype=np.int16).tobytes())