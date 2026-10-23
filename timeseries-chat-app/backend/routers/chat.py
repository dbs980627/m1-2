from fastapi import APIRouter, HTTPException
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS
from schemas import ChatRequest
from services import data_service, conv_service
from services.summary import summary_to_text

router = APIRouter(prefix="/api/chat", tags=["chat"])

SYSTEM = (
    "당신은 사용자의 시계열 데이터를 분석해 주는 도우미입니다.\n"
    "아래 [데이터 요약]만을 근거로 한국어로 간결하게 답하고, 요약에 없는 내용은 모른다고 말하세요.\n\n"
    "[데이터 요약]\n{summary}"
)


@router.post("")
def chat(req: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(500, "OPENAI_API_KEY가 설정되지 않았습니다.")
    try:
        # 1) 요약 조회 → 2) 시스템 프롬프트 삽입
        system = SYSTEM.format(summary=summary_to_text(data_service.summary()))
        history = [m.model_dump() for m in req.history][-10:]  # 토큰 절약
        msgs = [{"role": "system", "content": system}, *history, {"role": "user", "content": req.message}]
        # 3) GPT 호출
        res = OpenAI(api_key=OPENAI_API_KEY).chat.completions.create(
            model=OPENAI_MODEL, messages=msgs, max_tokens=MAX_TOKENS, temperature=0.3)
        reply = res.choices[0].message.content or ""
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"AI 응답 생성 실패: {type(e).__name__}")

    # 4) 자동 저장
    full = history + [{"role": "user", "content": req.message}, {"role": "assistant", "content": reply}]
    conv_id = req.conversation_id
    if not (conv_id and conv_service.save_messages(conv_id, full)):
        conv_id = conv_service.create(req.message[:30], full)
    return {"reply": reply, "conversation_id": conv_id}
