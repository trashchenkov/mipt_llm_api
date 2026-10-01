"""Запуск mitmproxy для наблюдения участка Б (GPT2GIGA → GigaChat). Необязательный шаг.

    uv run tools/start_mitmproxy.py

mitmproxy запускается через uvx — отдельно ставить ничего не нужно, Docker не нужен.
Запускать ДО tools/run_proxy.py: тот увидит mitmproxy и направит запросы через него.
- запрос токена (ngw.devices.sberbank.ru) проходит без расшифровки и в интерфейсе не виден;
- в запросах к модели заголовок Authorization в интерфейсе заменяется на «***» (tools/mitm_mask.py);
- показываются только запросы /chat/completions.
Остановка — Ctrl+C.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MITMPROXY = "mitmproxy==12.2.3"


def main():
    uvx = shutil.which("uvx")
    if uvx is None:
        print("uvx не найден — mitmproxy пропускаем. Занятию это не мешает: участок А виден в ноутбуке.")
        return
    command = [
        uvx, "--from", MITMPROXY, "mitmweb",
        "--listen-host", "127.0.0.1", "--listen-port", "8080",
        "--web-host", "127.0.0.1", "--web-port", "8081",
        "--ssl-insecure",
        "--ignore-hosts", r"^ngw\.devices\.sberbank\.ru",
        "--set", "view_filter=~u /chat/completions",
        "--set", "web_open_browser=false",
        "-s", str(ROOT / "tools" / "mitm_mask.py"),
    ]
    print("Запуск mitmproxy на 127.0.0.1:8080, интерфейс — http://127.0.0.1:8081")
    print("Ссылку с токеном для входа в интерфейс mitmweb напечатает ниже. Не показывайте её на трансляции.")
    print("Остановка — Ctrl+C.\n", flush=True)
    try:
        sys.exit(subprocess.call(command, cwd=ROOT))
    except KeyboardInterrupt:
        print("\nmitmproxy остановлен.")
    except OSError as error:
        print(f"mitmproxy не запустился ({error}). Занятию это не мешает: участок А виден в ноутбуке.")


if __name__ == "__main__":
    main()
