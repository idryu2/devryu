// 가이드라인 Q&A (RAG): 자연어 질문 → 근거 인용 답변 + 출처 + "참고용" 배너
import { useState } from "react";

import { useAsk } from "../api/hooks";

const EXAMPLES = [
  "CKD 환자에서 metformin은 어떻게 조정하나요?",
  "페니실린 알레르기 폐렴 환자의 항생제 선택은?",
  "와파린과 NSAID 병용 시 주의점은?",
  "임신부 고혈압 1차 약제는?",
];

export default function GuidelineQAPage() {
  const [q, setQ] = useState("");
  const ask = useAsk();

  const submit = (question: string) => {
    setQ(question);
    if (question.trim()) ask.mutate(question);
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-xl font-bold mb-1">가이드라인 Q&A</h1>
      <div className="bg-blue-50 border border-blue-200 text-blue-700 text-sm rounded p-2 mb-4">
        ℹ 본 답변은 RAG 기반 <b>참고용</b> 정보이며, 출처를 함께 표시합니다. 임상 결정은 검증이 필요합니다.
      </div>

      <div className="flex gap-2 mb-3">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit(q)}
          placeholder="질문을 입력하세요"
          className="flex-1 border border-slate-300 rounded px-3 py-2 text-sm"
        />
        <button onClick={() => submit(q)} className="px-4 py-2 bg-slate-900 text-white rounded text-sm">
          질문
        </button>
      </div>

      <div className="flex flex-wrap gap-2 mb-5">
        {EXAMPLES.map((e) => (
          <button
            key={e}
            onClick={() => submit(e)}
            className="text-xs px-2 py-1 bg-white border border-slate-200 rounded hover:border-slate-400"
          >
            {e}
          </button>
        ))}
      </div>

      {ask.isPending && <p className="text-slate-400">답변 생성 중…</p>}
      {ask.isError && <p className="text-red-600">오류: {String((ask.error as Error).message)}</p>}

      {ask.data && (
        <div className="bg-white border border-slate-200 rounded-lg p-4">
          <p className="whitespace-pre-wrap text-slate-800">{ask.data.answer}</p>
          <div className="mt-4">
            <div className="text-xs font-semibold text-slate-500 uppercase mb-1">출처</div>
            <ul className="space-y-1">
              {ask.data.sources.map((s, i) => (
                <li key={i} className="text-sm text-slate-600">
                  📄 <b>{s.source_label}</b> · {s.doc_title} — {s.section}
                </li>
              ))}
            </ul>
          </div>
          <p className="text-xs text-amber-600 mt-3">{ask.data.disclaimer}</p>
        </div>
      )}
    </div>
  );
}
