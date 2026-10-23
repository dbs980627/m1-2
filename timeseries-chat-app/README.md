# 데이터 기반 AI 채팅

시계열 데이터(예: 일별 학습 시간)를 Firestore에 저장·관리하고, 데이터 **요약(기간/개수/평균/최대/최소/추세)을 시스템 프롬프트에 주입**해 GPT가 내 데이터에 근거해 답하는 챗봇 서비스입니다. 대화는 자동 저장되며 다시 불러올 수 있습니다.

## 기술 스택
- Backend: Python 3.10+, FastAPI, Pydantic, firebase-admin(Firestore), openai
- Frontend: HTML / CSS / Vanilla JS
- 배포: Render(백엔드), Vercel(프론트)

## 배포 URL
- Frontend: https://YOUR-APP.vercel.app
- Backend API: https://YOUR-API.onrender.com
- Swagger: https://YOUR-API.onrender.com/docs
> 무료 Render는 15분 미사용 시 슬립 → 첫 요청이 최대 1분 지연됩니다. 화면에 안내 문구가 표시됩니다.

## 프로젝트 구조
```
backend/  main.py, config.py, firebase.py, schemas.py, seed.py
          routers/ (data, conversations, chat)   # HTTP 계층
          services/ (data_service, conv_service, summary)  # 비즈니스/DB 로직
frontend/ index.html, style.css, app.js, build.js, vercel.json
```

## API
| Method | Path | 설명 |
|---|---|---|
| POST/GET | /api/data | 추가 / 목록 |
| PUT/DELETE | /api/data/{id} | 수정 / 삭제 |
| GET | /api/data/summary | 요약(프롬프트 주입용) |
| POST/GET | /api/conversations | 저장 / 목록(messages 미포함) |
| GET/DELETE | /api/conversations/{id} | 전체 messages 조회 / 삭제 |
| POST | /api/chat | 요약 주입 → GPT → 자동 저장 |

## 로컬 실행
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # 값 채우기
python seed.py            # 샘플 데이터 120개 (선택)
uvicorn main:app --reload # http://localhost:8000/docs

cd ../frontend
python -m http.server 5500  # http://localhost:5500  (config.js의 주소 확인)
```

## 환경 변수
| 이름 | 위치 | 설명 |
|---|---|---|
| OPENAI_API_KEY | Render | OpenAI 키 |
| OPENAI_MODEL | Render | 기본 gpt-4o-mini (선택) |
| FIREBASE_SERVICE_ACCOUNT_JSON | Render | 서비스 계정 JSON **전체 문자열** (로컬은 파일 경로 가능) |
| ALLOWED_ORIGINS | Render | CORS 허용 도메인, 쉼표 구분 (예: https://YOUR-APP.vercel.app) |
| API_BASE_URL | Vercel | 백엔드 URL (빌드 시 config.js 생성) |

## 배포
- **Render**: GitHub 푸시 → New Web Service → Root Directory `backend`, Build `pip install -r requirements.txt`, Start `uvicorn main:app --host 0.0.0.0 --port $PORT`, 환경변수 등록.
- **Vercel**: Root Directory `frontend`, 환경변수 `API_BASE_URL` 설정 후 배포(`vercel.json`이 `node build.js` 실행).
- 배포 후 Render의 `ALLOWED_ORIGINS`에 Vercel 도메인을 추가하세요.

## 제출 스크린샷
1. 데이터 요약이 보이는 채팅 화면 (질문+답변)
2. 데이터 관리 화면 (CRUD 동작)
3. 대화 기록 화면 (불러오기)
