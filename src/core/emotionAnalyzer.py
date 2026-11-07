import threading
from pysentimiento import create_analyzer

analyzer = create_analyzer(task="emotion", lang="pt")

MAPA_PLUTCHIK = {
    "joy": "joy",
    "sadness": "sadness",
    "anger": "anger",
    "fear": "fear",
    "surprise": "surprise",
    "disgust": "disgust",
}

def apply_emotion(texto: str, affect):
    def _run():
        try:
            result = analyzer.predict(texto)
            for nome_pysent, prob in result.probas.items():
                nome_plutchik = MAPA_PLUTCHIK.get(nome_pysent)
                if nome_plutchik and prob >= 0.3: # filtra ruído
                    affect.on_user_emotion_detected(
                        nome_plutchik, prob, trust_level=0.5
                    )
        except Exception as e:
            print(f"[emotion] falhou: {e}")

    threading.Thread(target=_run, daemon=True).start()