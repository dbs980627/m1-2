import json
import firebase_admin
from firebase_admin import credentials, firestore
from config import FIREBASE_SERVICE_ACCOUNT_JSON

_db = None


def get_db():
    """Firestore 클라이언트 (지연 초기화). 키는 환경변수(JSON 문자열 또는 파일 경로)로만 받는다."""
    global _db
    if _db is None:
        raw = FIREBASE_SERVICE_ACCOUNT_JSON.strip()
        if not raw:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_JSON 환경변수가 설정되지 않았습니다.")
        cred = credentials.Certificate(json.loads(raw) if raw.startswith("{") else raw)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db
