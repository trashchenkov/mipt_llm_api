"""Проверка окружения перед занятием.

    uv run tools/check_env.py

Ничего не меняет. Значения ключей не печатает. Делает один запрос за токеном GigaChat.
"""
import os
import socket
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY_URL = "https://developers.sber.ru/studio/workspaces/my-space/get/gigachat-api"
PACKAGES = ["gigachat", "langchain-gigachat", "langchain-core", "openai", "anthropic", "httpx2", "jupyterlab"]
problems = 0


def ok(text):
    print(f"  ✓ {text}")


def fail(text, hint):
    global problems
    problems += 1
    print(f"  ✗ {text}\n    → {hint}")


def port_open(port):
    with socket.socket() as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


print("Python и пакеты")
if sys.version_info[:2] == (3, 12):
    ok(f"Python {sys.version.split()[0]}")
else:
    fail(f"Python {sys.version.split()[0]}, нужен 3.12", "запускайте через uv: uv sync, затем uv run …")
for package in PACKAGES:
    try:
        ok(f"{package} {version(package)}")
    except PackageNotFoundError:
        fail(f"{package} не установлен", "выполните uv sync в папке llm_api_to_langchain")

print("\nФайл .env")
env_file = ROOT / ".env"
if not env_file.is_file():
    fail(".env не найден", "cp .env.example .env и заполните GIGACHAT_CREDENTIALS")
else:
    from dotenv import load_dotenv

    load_dotenv(env_file, override=False)
    for key in ("GIGACHAT_CREDENTIALS", "GIGACHAT_SCOPE", "GIGACHAT_MODEL"):
        if os.getenv(key):
            ok(f"{key} задан")
        else:
            hint = f"ключ авторизации выдают в личном кабинете: {KEY_URL}" if key == "GIGACHAT_CREDENTIALS" \
                else "заполните по .env.example"
            fail(f"{key} не задан", hint)

print("\nДоступ к GigaChat")
if os.getenv("GIGACHAT_CREDENTIALS"):
    try:
        import gigachat

        with gigachat.GigaChat() as client:
            client.get_token()
        ok("токен получен (значение не печатаем)")
    except Exception as error:  # noqa: BLE001 — показываем любую причину
        name = type(error).__name__
        hint = {
            "AuthenticationError": f"ключ неверный или не тот scope; новый ключ — {KEY_URL}",
            "ConnectError": "нет сети до ngw.devices.sberbank.ru:9443 — проверьте VPN/прокси",
        }.get(name, "см. текст ошибки")
        fail(f"токен не получен: {name}", hint)
else:
    print("  – пропущено: нет ключа")

print("\nПрокси и наблюдение")
port = int(os.getenv("GPT2GIGA_PORT", "8090"))
if port_open(port):
    ok(f"GPT2GIGA отвечает на 127.0.0.1:{port}")
else:
    fail(f"GPT2GIGA не запущен на 127.0.0.1:{port}", "во втором терминале: uv run tools/run_proxy.py")
if port_open(8080):
    ok("mitmproxy запущен (участок Б виден в http://127.0.0.1:8081)")
else:
    print("  – mitmproxy не запущен — это необязательно")

print("\nИтог:", "всё готово" if problems == 0 else f"проблем: {problems}")
sys.exit(1 if problems else 0)
