"""Детерминированный учебный инструмент. Данные вымышлены."""

ROOMS = {
    "A-101": {"capacity": 24, "projector": True},
    "B-202": {"capacity": 40, "projector": False},
}


def get_room_info(room: str) -> dict:
    """Вернуть вместимость и наличие проектора в учебной аудитории."""
    if not isinstance(room, str) or room not in ROOMS:
        raise ValueError(f"Неизвестная аудитория: {room!r}; в справочнике: {', '.join(ROOMS)}")
    return {"room": room, **ROOMS[room]}


def execute_tool(name: str, arguments: dict) -> dict:
    """Разрешён ровно один инструмент и один строковый аргумент."""
    if name != "get_room_info":
        raise ValueError("Неизвестный инструмент")
    if not isinstance(arguments, dict) or set(arguments) != {"room"}:
        raise ValueError("Ожидается только аргумент room")
    return get_room_info(arguments["room"])
