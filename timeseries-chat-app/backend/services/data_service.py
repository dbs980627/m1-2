from firebase import get_db
from services.summary import build_summary

COL = "data"


def _doc(d):
    x = d.to_dict()
    return {"id": d.id, "date": x["date"], "value": x["value"], "memo": x.get("memo", "")}


def list_data():
    docs = get_db().collection(COL).order_by("date").stream()
    return [_doc(d) for d in docs]


def create(item):
    ref = get_db().collection(COL).document()
    ref.set({"date": item.date.isoformat(), "value": item.value, "memo": item.memo})
    return _doc(ref.get())


def update(doc_id, item):
    ref = get_db().collection(COL).document(doc_id)
    if not ref.get().exists:
        return None
    ref.update({"date": item.date.isoformat(), "value": item.value, "memo": item.memo})
    return _doc(ref.get())


def delete(doc_id):
    ref = get_db().collection(COL).document(doc_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True


def summary():
    return build_summary(list_data())
