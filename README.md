# Разработка и внедрение AI-агентов · МФТИ

Материалы занятий, которые в курсе ведёт Тращенков Сергей.
Telegram-канал: [t.me/gigatrash](https://t.me/gigatrash).

**Версии материалов.** Блокноты используют закреплённые версии библиотек проведённых занятий.
`uv sync` устанавливает их из `uv.lock`. [Обзор изменений на 16.11.2026](UPDATES.md) объясняет поведение новых версий;
рядом с соответствующими примерами в блокнотах есть пояснения.

| Тема | Папка |
|---|---|
| От API языковой модели к LangChain | [llm_api_to_langchain](llm_api_to_langchain/) |
| LangChain и Deep Agents | [langchain_deep_agents](langchain_deep_agents/) |

## Что понадобится

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — ставит Python и зависимости.
- Ключ авторизации GigaChat API. Его выдают в
  [личном кабинете](https://developers.sber.ru/studio/workspaces/my-space/get/gigachat-api):
  проект GigaChat API → «Настройки API» → «Получить ключ»
  ([инструкция](https://developers.sber.ru/docs/ru/gigachat/quickstart/ind-create-project)).
  Ключ показывается один раз — сохраните его сразу.

Порядок установки — в README каждой папки.
