import atexit
import subprocess
import httpx
import time

def wait_server(porta=8080):
    url = f"http://127.0.0.1:{porta}/health"

    for _ in range(120):
        try:
            response = httpx.get(url, timeout=10)

            if response.status_code == 200:
                print("Amadeus is Ready!")
                return True
        except (httpx.ConnectError, httpx.ReadTimeout):
            pass

        time.sleep(1)
    print("Waited more than 2 minutes to amadeus wake up")
    return False


class ServerManager:
    def __init__(self, SERVER_EXE, MODEL_GGUF):
        self.process = None
        self.cmd = [
            SERVER_EXE,
            "-m", MODEL_GGUF,
            "-ngl", "99",
            "-c", "8192",
            "--jinja",
            "-fa", "off",
            "--no-reasoning-preserve",
            "--reasoning-budget", "0",
            "--host", "127.0.0.1",
            "--port", "8080",
        ]

    def start(self):
        print("Initializing server...")
        self.process = subprocess.Popen(
            self.cmd,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        atexit.register(self.stop)
    def stop(self):
        if self.process:
            self.process.terminate()
