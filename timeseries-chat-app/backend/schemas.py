from datetime import date as Date
from typing import List, Optional
from pydantic import BaseModel, Field


class DataIn(BaseModel):
    date: Date
    value: float
    memo: str = Field(default="", max_length=200)


class DataOut(BaseModel):
    id: str
    date: str
    value: float
    memo: str = ""


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=4000)


class ConversationIn(BaseModel):
    title: str = Field(default="새 대화", max_length=100)
    messages: List[Message]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    conversation_id: Optional[str] = None
    history: List[Message] = []
