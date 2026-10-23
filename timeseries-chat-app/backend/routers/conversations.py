from fastapi import APIRouter, HTTPException
from schemas import ConversationIn
from services import conv_service as svc

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.post("", status_code=201)
def save_conversation(body: ConversationIn):
    return {"id": svc.create(body.title, [m.model_dump() for m in body.messages])}


@router.get("")
def list_conversations():
    return svc.list_all()


@router.get("/{conv_id}")
def get_conversation(conv_id: str):
    c = svc.get(conv_id)
    if not c:
        raise HTTPException(404, "대화를 찾을 수 없습니다.")
    return c


@router.delete("/{conv_id}")
def delete_conversation(conv_id: str):
    if not svc.delete(conv_id):
        raise HTTPException(404, "대화를 찾을 수 없습니다.")
    return {"deleted": conv_id}
