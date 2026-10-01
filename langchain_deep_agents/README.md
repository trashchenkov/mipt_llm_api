# LangChain и Deep Agents

Продолжение занятия [«От API языковой модели к LangChain»](../llm_api_to_langchain/). Тот же вопрос —
«Поместятся ли 28 студентов в аудитории A-101?» — теперь решает агент: сначала `create_agent` из
LangChain, затем обвязка Deep Agents с планом, файлами, командной строкой, субагентами и памятью.
Отдельно — middleware: как управлять агентом и подстраивать его под GigaChat.

## Материалы

- [Ноутбук занятия](langchain_deep_agents.ipynb).
- [Слайды (PDF)](langchain_deep_agents.pdf).
- [Документация и исходники](SOURCES.md).
- [Решение упражнения](solutions/tool_errors.py) — после собственной попытки.

## 1. Установка

Нужен [uv](https://docs.astral.sh/uv/getting-started/installation/). Команды одинаковы для macOS, Linux и Windows.

Папка уже есть в репозитории, склонированном на прошлом занятии. Из папки `llm_api_to_langchain`:

```bash
cd ../langchain_deep_agents
uv sync
```

Если репозитория нет: `git clone https://github.com/trashchenkov/mipt_llm_api`, затем
`cd mipt_llm_api/langchain_deep_agents` и `uv sync`.

`uv sync` сам поставит Python 3.12 и точные версии библиотек из `uv.lock`.

## 2. Настройки: `.env`

Отдельно настраивать ничего не нужно: если в этой папке нет своего `.env`, ноутбук и
`tools/check_env.py` берут `.env` прошлого занятия из `../llm_api_to_langchain/`.

Свой `.env` нужен, если прошлое занятие вы пропустили или хотите здесь другие настройки — он
важнее соседнего:

```bash
cp .env.example .env          # Windows: copy .env.example .env
```

В нём заполните `GIGACHAT_CREDENTIALS` — ключ авторизации GigaChat API из
[личного кабинета](https://developers.sber.ru/studio/workspaces/my-space/get/gigachat-api).

Не публикуйте `.env`: он добавлен в `.gitignore`.

## 3. Проверка и запуск

```bash
uv run tools/check_env.py
uv run jupyter lab langchain_deep_agents.ipynb
```

Прокси GPT2GIGA на этом занятии не нужен.

## Командная строка агента

В разделе 9 агент выполняет команды в командной строке вашего компьютера. Файлы он пишет в папку
`workspace/` рядом с ноутбуком; её можно удалить после занятия.

## Если что-то не работает

| Симптом | Что проверить |
|---|---|
| `check_env` пишет про ключ | Ключ в `.env`, scope `GIGACHAT_API_PERS` |
| Нет строки `Harness profile loaded` | Пакет `deepagents-gigachat` установлен: `uv sync` |
| Агент не ведёт план | Подключён ли `TodoListMiddleware` и есть ли в задаче просьба составить план |
| Ответ отличается от соседа | Это нормально: сравнивайте шаги агента и данные |
