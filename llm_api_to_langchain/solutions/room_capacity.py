"""Решение упражнения 7.1: новый факт с исходным идентификатором вызова."""
import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from room_tool import ROOMS, execute_tool


def solve(llm, ai_message, question, system):
    """Один реальный запрос после изменения данных; восстановление даже при ошибке."""
    calls = ai_message.tool_calls
    if len(calls) != 1:
        raise ValueError("Для упражнения нужен ровно один вызов")
    call = calls[0]
    if call["name"] != "get_room_info" or call["args"] != {"room": "A-101"}:
        raise ValueError("Ожидается вызов get_room_info для A-101")
    if not call.get("id"):
        raise ValueError("Нужен идентификатор реального вызова")
    original_capacity = ROOMS["A-101"]["capacity"]
    try:
        ROOMS["A-101"]["capacity"] = 32
        updated = execute_tool(call["name"], call["args"])
        result = ToolMessage(
            content=json.dumps(updated, ensure_ascii=False),
            tool_call_id=call["id"],
            name=call["name"],
        )
        return llm.invoke([
            SystemMessage(content=system), HumanMessage(content=question), ai_message, result,
        ])
    finally:
        ROOMS["A-101"]["capacity"] = original_capacity
