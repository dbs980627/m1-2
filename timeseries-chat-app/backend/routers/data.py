from typing import List
from fastapi import APIRouter, HTTPException
from schemas import DataIn, DataOut
from services import data_service as svc

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/summary")
def get_summary():
    return svc.summary()


@router.get("", response_model=List[DataOut])
def list_data():
    return svc.list_data()


@router.post("", response_model=DataOut, status_code=201)
def create_data(item: DataIn):
    return svc.create(item)


@router.put("/{doc_id}", response_model=DataOut)
def update_data(doc_id: str, item: DataIn):
    r = svc.update(doc_id, item)
    if r is None:
        raise HTTPException(404, "데이터를 찾을 수 없습니다.")
    return r


@router.delete("/{doc_id}")
def delete_data(doc_id: str):
    if not svc.delete(doc_id):
        raise HTTPException(404, "데이터를 찾을 수 없습니다.")
    return {"deleted": doc_id}
