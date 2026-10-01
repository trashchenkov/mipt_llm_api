"""Запуск GPT2GIGA для занятия.

    uv run tools/run_proxy.py

Прокси запускается через uvx с закреплёнными версиями (requirements-proxy.txt), настройки — из .env.
Если на 127.0.0.1:8080 уже работает mitmproxy (tools/start_mitmproxy.py), запросы прокси к GigaChat
идут через него (участок Б). Если нет — прокси работает напрямую, ничего не ломается.
Остановка — Ctrl+C.
"""
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
CONSTRAINTS = ROOT / "requirements-proxy.txt"
MITM_HOST, MITM_PORT, MITM_WEB_PORT = "127.0.0.1", 8080, 8081


def port_open(host, port):
    with socket.socket() as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def proxy_command(env_file=None):
    """Команда запуска GPT2GIGA 0.3.0 через uvx с закреплёнными зависимостями."""
    uvx = shutil.which("uvx")
    if uvx is None:
        sys.exit("Не найден uvx. Установите uv: https://docs.astral.sh/uv/getting-started/installation/")
    command = [uvx, "--python", "3.12", "--from", "gpt2giga==0.3.0", "--constraints", str(CONSTRAINTS), "gpt2giga"]
    if env_file is not None:
        # Абсолютный путь обязателен: GPT2GIGA ищет относительный .env от папки своего кода,
        # а при запуске через uvx код лежит в кэше uv и файл не находится.
        command += ["--env-path", str(Path(env_file).resolve())]
    return command


def main():
    if not ENV_FILE.is_file():
        sys.exit(f"Нет файла {ENV_FILE}. Скопируйте шаблон: cp .env.example .env и заполните ключ.")
    env = dict(os.environ)
    if port_open(MITM_HOST, MITM_PORT):
        proxy = f"http://{MITM_HOST}:{MITM_PORT}"
        env.update(HTTP_PROXY=proxy, HTTPS_PROXY=proxy, NO_PROXY="localhost,127.0.0.1", no_proxy="localhost,127.0.0.1")
        print("mitmproxy найден: запросы к GigaChat идут через него (участок Б).")
        print(f"Интерфейс mitmproxy: http://{MITM_HOST}:{MITM_WEB_PORT}")
    else:
        print("mitmproxy не запущен: участок Б не наблюдаем, прокси работает напрямую.")

    command = proxy_command(ENV_FILE)
    print("Запуск GPT2GIGA… Остановка — Ctrl+C.\n", flush=True)
    try:
        sys.exit(subprocess.call(command, cwd=ROOT, env=env))
    except KeyboardInterrupt:
        print("\nGPT2GIGA остановлен.")


if __name__ == "__main__":
    main()
