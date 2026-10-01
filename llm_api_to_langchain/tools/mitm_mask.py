"""Дополнение mitmproxy: скрывает токен в интерфейсе.

Заголовок Authorization заменяется на «Bearer ***» после того, как запрос уже отправлен
и ответ получен, — сам запрос к GigaChat не меняется.
"""


def response(flow):
    if "authorization" in flow.request.headers:
        flow.request.headers["authorization"] = "Bearer ***"
