"""LLM 공급자 추상 인터페이스.

★ LLM은 보조 역할만 한다(경고 설명, 가이드라인 Q&A). 환자 안전 판단에는 절대
사용하지 않는다. 모든 출력에는 호출부에서 "참고용 · 검증 필요" 표시를 붙인다.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# LLM 출력에 항상 동반되는 면책 문구
DISCLAIMER = "※ 본 설명은 LLM이 생성한 참고용 정보이며 임상적 검증이 필요합니다."


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def explain_alert(self, alert: dict, patient: dict) -> str:
        """결정론적 규칙 엔진이 생성한 경고를 임상의가 이해하기 쉽게 자연어로 설명."""

    @abstractmethod
    def answer_question(self, question: str, contexts: list[dict]) -> str:
        """RAG 근거(contexts)를 바탕으로 가이드라인 질문에 답변. 출처는 호출부가 부착."""
