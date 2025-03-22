from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import WebSocket
import jwt
from pydantic import BaseModel
from pydantic import ValidationError
from starlette.websockets import WebSocketDisconnect

from app.core.config import settings
from app.services import ChatService
from app.utils import UnitOfWork

router = APIRouter()
# (socket, user_id)
connections = []
# (from (id), message, to (id))
messages = []


class Message(BaseModel):
    message: str
    to_user: int
    files: list | None = None


def get_jwt_payload(token: str) -> dict | str:
    """
    This function decodes token
    if token invalid :return: name of error
    else :return: payload(json)
    :param token: str
    """
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ENCRYPT_ALG])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Bearer token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid bearer token")


# TODO: Сделать сохранение, и выгрузку чата из db
@router.websocket("/chat")
async def chat(socket: WebSocket):
    payload = get_jwt_payload(socket.headers.get("Authorization").split("$")[1])
    await socket.accept()
    connections.append((socket, payload["sub"]))
    db = ChatService(UnitOfWork())
    to_send = await db.get_all_to_user(int(payload["sub"]))
    for i in to_send:
        await socket.send_json({"from": i.from_user,
                                "message": i.text})
    try:
        while True:
            try:
                data = Message(**(await socket.receive_json()))
                await db.save_message(int(payload["sub"]), to_user=data.to_user, message=data.message, files=data.files)
            except ValidationError:
                error = {}
                await socket.send_json(error)
                continue
            socket_to_send = list(filter(lambda x: int(x[1]) == int(data.to_user), connections))
            if socket_to_send:
                socket_to_send = list(socket_to_send)[0][0]
                await socket_to_send.send_json({"from": payload["sub"],
                                                "message": data.message})
            else:
                messages.append((payload["sub"], data.message, data.to_user))
    except WebSocketDisconnect:
        connections.remove((socket, payload["sub"]))
