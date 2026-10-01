"""Решение упражнения: ошибка инструмента возвращается модели, а не обрывает запуск агента."""
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage


@wrap_tool_call
def tool_errors_to_model(request, handler):
    try:
        return handler(request)
    except ValueError as error:
        return ToolMessage(content=f"Ошибка: {error}", tool_call_id=request.tool_call["id"],
                           name=request.tool_call["name"], status="error")
