# От API языковой модели к LangChain

Один вопрос — «Поместятся ли 28 студентов в аудитории A-101?» — проходит через GigaChat API,
три популярных формата обмена (OpenAI Chat Completions, OpenAI Responses, Anthropic Messages)
и LangChain. Смотрим, что уходит по сети, где в ответе текст и вызов функции и кто эту функцию исполняет.

## Материалы

- [Ноутбук занятия](llm_api_to_langchain.ipynb).
- [Слайды (PDF)](llm_api_to_langchain.pdf).
- [Наблюдение HTTP-запросов](HTTP_OBSERVATION.md): что видно в ноутбуке и через mitmproxy.
- [Документация и исходники](SOURCES.md).
- [Решение упражнения](solutions/room_capacity.py) — после собственной попытки.

## 1. Установка

Нужен [uv](https://docs.astral.sh/uv/getting-started/installation/). Команды одинаковы для macOS, Linux и Windows.

```bash
git clone https://github.com/trashchenkov/mipt_llm_api
cd mipt_llm_api/llm_api_to_langchain
uv sync
cp .env.example .env          # Windows: copy .env.example .env
```

`uv sync` сам поставит Python 3.12 и точные версии библиотек из `uv.lock`.

## 2. Настройки: `.env`

Заполните `GIGACHAT_CREDENTIALS` — ключ авторизации GigaChat API. Ключ выдают в
[личном кабинете](https://developers.sber.ru/studio/workspaces/my-space/get/gigachat-api):
проект GigaChat API → «Настройки API» → «Получить ключ»
([инструкция](https://developers.sber.ru/docs/ru/gigachat/quickstart/ind-create-project)).
Ключ показывается один раз. Остальные значения в шаблоне уже подходят для занятия.

Не публикуйте `.env`: он добавлен в `.gitignore`.

## 3. Проверка и запуск

Проверить окружение (ключ, пакеты, доступ к GigaChat):

```bash
uv run tools/check_env.py
```

Во **втором терминале** — прокси GPT2GIGA, через него работают библиотеки OpenAI и Anthropic:

```bash
uv run tools/run_proxy.py
```

В первом терминале — Jupyter:

```bash
uv run jupyter lab llm_api_to_langchain.ipynb
```

Необязательно: наблюдение запросов прокси к GigaChat через mitmproxy. Запускать **до** прокси,
в третьем терминале:

```bash
uv run tools/start_mitmproxy.py
```

Прокси и mitmproxy останавливаются клавишами `Ctrl+C` в своих терминалах.

## Если что-то не работает

| Симптом | Что проверить |
|---|---|
| `check_env` пишет про ключ | Ключ в `.env`, scope `GIGACHAT_API_PERS` |
| `Connection refused` в ноутбуке | Запущен ли `tools/run_proxy.py` во втором терминале |
| Нет вызова инструмента | Реальный ответ модели и причину завершения |
| Ответ отличается от соседа | Это нормально: модель каждый раз пишет текст заново; сравнивайте структуру ответа и данные |
