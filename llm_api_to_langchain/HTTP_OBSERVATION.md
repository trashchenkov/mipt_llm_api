# Наблюдение HTTP: до и после GPT2GIGA

## 1. Два участка, два формата

```text
SDK OpenAI/Anthropic  ── A ──►  GPT2GIGA  ── B ──►  GigaChat API
                     ◄─────             ◄─────
```

- **A:** исходный клиентский контракт — Chat Completions, Responses или Messages.
- **B:** преобразованный запрос GigaChat и ответ GigaChat до обратного преобразования.

Сравнивайте один и тот же вызов по обе стороны. Python-словарь до вызова SDK
не равен захвату HTTP: SDK сериализует body и добавляет свои поля.

## 2. Вход A: прямо в notebook, без Docker

В разделе 2 notebook подключает `request` event hook транспортного клиента. Hook
печатает метод, путь и полное подготовленное UTF-8 body:

```python
from html import escape
from IPython.display import HTML, display

def print_http_request(request):
    print(f"HTTP → {request.method} {request.url.path}")
    body = request.content.decode("utf-8")
    display(HTML(
        f"<details><summary>Тело HTTP-запроса</summary><pre>{escape(body)}</pre></details>"
    ))
```

В `<details>` попадает то же сериализованное body, которое подготовил SDK, без
повторного `json.dumps`, prettify или нормализации порядка полей. `escape` нужен
только для безопасного отображения в HTML. Полный response JSON также сохраняется
в раскрываемом блоке: сначала смотрим ключевые поля, затем при необходимости
открываем полный ответ.

Hook показывает запрос, подготовленный к передаче в транспорт. Что сервер получил
именно эти байты, подтверждает перехват на его стороне — участок Б.

Не выводим headers/query: там могут быть данные авторизации. Body тоже может
содержать личные данные, поэтому нужны учебные prompts и очистка outputs перед
публикацией. В установленных версиях SDK используется `httpx2.Client`; это
транспортная зависимость, не отдельный API-адаптер. Hook подключён к клиентам
прокси, а не к прямому GigaChat SDK или LangChain-клиенту.

Источники: [HTTPX request hooks](https://www.python-httpx.org/advanced/event-hooks/),
[HTTPX2](https://github.com/pydantic/httpx2),
[OpenAI SDK HTTP client](https://github.com/openai/openai-python#configuring-the-http-client),
[Anthropic SDK HTTP client](https://github.com/anthropics/anthropic-sdk-python#configuring-the-http-client).

## 3. Локальный GPT2GIGA в основном практикуме

Основной практикум запускает GPT2GIGA как локальный DEV-процесс на `127.0.0.1:8090`
с `GPT2GIGA_ENABLE_API_KEY_AUTH=False`. Отдельный proxy-secret не нужен. OpenAI и
Anthropic SDK получают техническое `api_key="unused"`, потому что их конструкторы
требуют значение, но локальный прокси его не проверяет.

Этот режим подходит только для локального занятия. Не публикуйте порт наружу и не
переносите отключённую авторизацию в общий стенд.

## 4. Вход A со стороны сервера: traffic logs

GPT2GIGA 0.3.0 умеет сохранять входящий JSON. Это **распарсенный и редактированный
объект**, не byte-for-byte копия исходного body: пробелы и исходное представление
не сохраняются. Это также не лог преобразованного upstream-запроса.

Для локальной отладки можно добавить в тот же `.env` и перезапустить GPT2GIGA:

```dotenv
GPT2GIGA_TRAFFIC_LOG_ENABLED=True
GPT2GIGA_TRAFFIC_LOG_SINK=jsonl
GPT2GIGA_TRAFFIC_LOG_JSONL_PATH=artifacts/traffic_logs.jsonl
GPT2GIGA_TRAFFIC_LOG_CAPTURE_CONTENT=True
GPT2GIGA_TRAFFIC_LOG_REDACT_SENSITIVE=True
```

Из папки `llm_api_to_langchain` перед запуском создайте `artifacts` (`mkdir -p artifacts`).
Лог удобен для подтверждения принятого запроса. Redaction не делает произвольные
prompts безопасными для публикации. После отладки выключите capture и не раздавайте лог.

Источники: [operations](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/docs/operations.md),
[чтение входного JSON](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/src/gpt2giga/common/request_json.py),
[сохранение отредактированного body](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/src/gpt2giga/sinks/logs/emission.py).

## 5. Выход B: mitmproxy

mitmproxy встаёт между GPT2GIGA и GigaChat и показывает запросы, которые прокси отправляет
в GigaChat, и ответы GigaChat до обратного преобразования. Docker не нужен: скрипты запускают
mitmproxy и прокси через `uvx`.

1. Третий терминал, из `llm_api_to_langchain`: `uv run tools/start_mitmproxy.py` — `mitmweb` на `127.0.0.1:8080`,
   интерфейс `http://127.0.0.1:8081` (ссылку для входа скрипт печатает при запуске).
2. Второй терминал: `uv run tools/run_proxy.py` — находит mitmproxy на 8080 и запускает GPT2GIGA
   с `HTTP_PROXY`/`HTTPS_PROXY` на него. Без mitmproxy прокси работает напрямую.

Настройки `start_mitmproxy.py`:
- `--ssl-insecure` и `GIGACHAT_VERIFY_SSL_CERTS=False` в `.env`: сертификаты на обоих плечах не проверяются,
  отдельный CA не нужен;
- `--ignore-hosts ^ngw\.devices\.sberbank\.ru`: запрос токена проходит без расшифровки и не виден;
- дополнение `tools/mitm_mask.py`: заголовок `Authorization` в интерфейсе заменяется на `Bearer ***`
  после отправки — сам запрос не меняется;
- фильтр отображения `~u /chat/completions`: в интерфейсе только запросы к модели.

Проверено 01.10.2026 (mitmproxy 12.2.3, GPT2GIGA 0.3.0): запросы в трёх форматах проходят через mitmproxy,
токен в интерфейсе скрыт.

## 6. Что искать в захвате

Для одного tool exchange сопоставьте:

1. A: описание инструмента и выбор функции в первом запросе SDK.
2. B: во что GPT2GIGA превратил эти поля для GigaChat.
3. Ответ B и преобразованный ответ A: где имя, аргументы и ID вызова.
4. Следующий запрос A с результатом локальной функции и соответствующий запрос B.

Что видно на участке Б (проверено 01.10.2026):
- Chat Completions, Responses и Messages превращаются в **одинаковый** запрос GigaChat v1:
  `functions`, `function_call` у ассистента, результат с ролью `function`.
- ID вызова (`tool_call_id`, `call_id`, `tool_use_id`) в GigaChat **не передаётся**: результат
  связывается с вызовом по имени функции.
- Результат инструмента строкой прокси оборачивает в `{"result": "..."}`.

Не публикуйте файлы перехвата, `.env` и ссылку для входа в интерфейс mitmweb.
