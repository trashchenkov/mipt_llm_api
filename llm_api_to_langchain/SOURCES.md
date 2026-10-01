# Документация и исходники

Материалы, на которые опирается занятие. Ссылки на GitHub закреплены на конкретных версиях
кода — тех, с которыми работает ноутбук.

## GigaChat API

- [Регистрация в личном кабинете](https://developers.sber.ru/docs/ru/gigachat/quickstart/ind-create-project) —
  как создать проект и получить ключ авторизации.
- [Личный кабинет: проект GigaChat API](https://developers.sber.ru/studio/workspaces/my-space/get/gigachat-api).
- [Справка GigaChat API](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/gigachat-api) —
  все методы: авторизация, модели, генерация, токены, баланс, файлы.
- [Сгенерировать ответ V2](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-chat-v-2) —
  поля запроса и ответа v2, параметры `model_options`, значения `finish_reason`.
- [Подсчёт токенов](https://developers.sber.ru/docs/ru/gigachat/guides/counting-tokens) — `usage`
  и тарификация закэшированных токенов.
- [Работа с историей чата](https://developers.sber.ru/docs/ru/gigachat/guides/keeping-context) —
  заголовок `X-Session-ID` и кэширование контекста.
- [Работа с функциями](https://developers.sber.ru/docs/ru/gigachat/guides/functions/overview) и
  [встроенные функции](https://developers.sber.ru/docs/ru/gigachat/guides/functions/calling-builtin-functions).

## SDK GigaChat (`gigachat` 0.2.3)

- [README](https://github.com/ai-forever/gigachat) — установка, способы авторизации, примеры.
- [Руководство по переходу на v2](https://github.com/ai-forever/gigachat/blob/efdc363a164b3a4def2f77af8c00bd4a73e4d971/MIGRATION_GUIDE.md) —
  методы `chat()` и `chat.create()`, модели запросов и ответов v1 и v2.
- [Настройки клиента](https://github.com/ai-forever/gigachat/blob/efdc363a164b3a4def2f77af8c00bd4a73e4d971/src/gigachat/settings.py) —
  какие переменные `GIGACHAT_*` читает SDK.

## Форматы OpenAI и Anthropic

- [Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) —
  справка по формату.
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling) — вызов функций
  в Chat Completions и Responses.
- [Переход на Responses](https://developers.openai.com/api/docs/guides/migrate-to-responses) — чем
  Responses отличается от Chat Completions.
- [Anthropic: Create a Message](https://platform.claude.com/docs/en/api/messages/create) — справка
  по формату Messages.
- [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) —
  блоки `tool_use` и `tool_result`.

## GPT2GIGA (0.3.0)

- [Репозиторий](https://github.com/ai-forever/gpt2giga) и
  [быстрый старт](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/docs/quickstart.md).
- [Совместимость API](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/docs/api-compatibility.md) —
  какие возможности форматов поддерживаются.
- [Настройки](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/docs/configuration.md) —
  переменные `GPT2GIGA_*`.
- Примеры вызова функций:
  [Responses](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/examples/openai/responses/tools/function_calling.py),
  [Messages](https://github.com/ai-forever/gpt2giga/blob/7b3d95dd2b853d555820658b2cc57fcda2af6523/examples/anthropic/messages/tools/function_calling.py).

## LangChain

- [Сообщения](https://docs.langchain.com/oss/python/langchain/messages) — `SystemMessage`,
  `HumanMessage`, `AIMessage`, `ToolMessage`.
- [Инструменты](https://docs.langchain.com/oss/python/langchain/tools) — `@tool` и `bind_tools`.
- [langchain-gigachat](https://github.com/ai-forever/langchain-gigachat/blob/b0c2ed0a18da778d6ec987e5280eb8b500d1e2bf/libs/gigachat/README.md) —
  интеграция GigaChat;
  [исходник адаптера](https://github.com/ai-forever/langchain-gigachat/blob/b0c2ed0a18da778d6ec987e5280eb8b500d1e2bf/libs/gigachat/langchain_gigachat/chat_models/gigachat.py)
  для приложения к ноутбуку.
- К следующему занятию: [агенты](https://docs.langchain.com/oss/python/langchain/agents),
  [middleware](https://docs.langchain.com/oss/python/langchain/middleware/overview),
  [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview).

## Инструменты

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — установка Python и зависимостей.
- [JSON Schema](https://json-schema.org/) — язык описания аргументов функций.
- [HTTPX: event hooks](https://www.python-httpx.org/advanced/event-hooks/) — как работает hook,
  которым ноутбук показывает тело запроса.
- [mitmproxy](https://docs.mitmproxy.org/stable/) — перехват HTTP(S)-трафика; как им пользоваться
  на занятии — в [HTTP_OBSERVATION.md](HTTP_OBSERVATION.md).
