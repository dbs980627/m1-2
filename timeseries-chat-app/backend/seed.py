"""샘플 데이터 120개(일별 학습 시간, 분) 업로드: python seed.py"""
import random
from datetime import date, timedelta
from firebase import get_db

random.seed(7)
db = get_db()
start = date.today() - timedelta(days=119)
batch, v = db.batch(), 90.0
for i in range(120):
    v = max(20, min(240, v + random.uniform(-15, 17)))
    ref = db.collection("data").document()
    batch.set(ref, {"date": (start + timedelta(days=i)).isoformat(), "value": round(v, 1), "memo": "샘플"})
    if (i + 1) % 400 == 0:
        batch.commit(); batch = db.batch()
batch.commit()
print("seeded 120 rows")