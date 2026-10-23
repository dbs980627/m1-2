from datetime import datetime, timezone
from firebase import get_db

COL = "conversations"


def _now():
    return datetime.now(timezone.utc).isoformat()


def create(title, messages):
    ref = get_db().collection(COL).document()
    ref.set({"title": title, "messages": messages, "created_at": _now(), "updated_at": _now()})
    return ref.id


def save_messages(conv_id, messages):
    ref = get_db().collection(COL).document(conv_id)
    if not ref.get().exists:
        return False
    ref.update({"messages": messages, "updated_at": _now()})
    return True


def list_all():
    """목록 응답에는 messages를 포함하지 않는다 (상세는 GET /{id})."""
    docs = get_db().collection(COL).order_by("updated_at", direction="DESCENDING").stream()
    out = []
    for d in docs:
        x = d.to_dict()
        out.append({"id": d.id, "title": x.get("title", ""), "updated_at": x.get("updated_at"),
                    "message_count": len(x.get("messages", []))})
    return out


def get(conv_id):
    d = get_db().collection(COL).document(conv_id).get()
    return {"id": d.id, **d.to_dict()} if d.exists else None


def delete(conv_id):
    ref = get_db().collection(COL).document(conv_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True
