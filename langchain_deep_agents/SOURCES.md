# Документация и исходники

Материалы, на которые опирается занятие.

## LangChain

- [Агенты](https://docs.langchain.com/oss/python/langchain/agents) — `create_agent`, агентный цикл.
- [Middleware: обзор](https://docs.langchain.com/oss/python/langchain/middleware/overview) — хуки и порядок вызова.
- [Встроенные middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in) — лимиты,
  суммаризация, подтверждение человеком, повторы и другие.
- [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) — прерывания и решения.
- [Память диалога](https://docs.langchain.com/oss/python/langchain/short-term-memory) — checkpointer и `thread_id`.

## LangGraph

- [Обзор](https://docs.langchain.com/oss/python/langgraph/overview) — графы, состояние, исполнение.
- [Прерывания](https://docs.langchain.com/oss/python/langgraph/interrupts) — `interrupt` и `Command(resume=...)`.

## Deep Agents

- [Обзор](https://docs.langchain.com/oss/python/deepagents/overview) — обвязка и её части.
- [Бэкенды](https://docs.langchain.com/oss/python/deepagents/backends) — где живут файлы агента.
- [Субагенты](https://docs.langchain.com/oss/python/deepagents/subagents).
- [Skills](https://docs.langchain.com/oss/python/deepagents/skills) и спецификация
  [agentskills.io](https://agentskills.io/specification).
- [Список изменений deepagents 0.7](https://github.com/langchain-ai/deepagents/pull/4929) — `write_todos`
  стал необязательным.

## GigaChat

- [langchain-gigachat](https://github.com/ai-forever/langchain-gigachat) — модель GigaChat в LangChain.
- [deepagents-gigachat](https://github.com/ai-forever/deepagents-gigachat) — профиль обвязки под GigaChat.
- [harness-bench-fast](https://github.com/ai-forever/harness-bench-fast) — набор задач для сравнения обвязок.
- Статьи на Хабре: [«Deep Agents: open source-обвязка на LangGraph»](https://habr.com/ru/companies/sberbank/articles/1071036/),
  [«Профиль GigaChat для Deep Agents»](https://habr.com/ru/companies/sberbank/articles/1073668/).
