// 우측 CDSS 경고 패널: 등급별 정렬 + 제목/설명/권고/근거 + [자세히(LLM)] + [확인(ack)]
import { useState } from "react";

import { useExplain } from "../api/hooks";
import { SEVERITY_STYLE, type Alert } from "../lib/api";

export default function AlertPanel({
  patientId,
  alerts,
  counts,
  isLoading,
  acked,
  onAck,
}: {
  patientId: string;
  alerts: Alert[];
  counts: Record<string, number>;
  isLoading: boolean;
  acked: Set<string>;
  onAck: (key: string) => void;
}) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="font-bold">CDSS 경고</h2>
        <div className="flex gap-1 text-xs">
          <Badge n={counts.CRITICAL ?? 0} cls="bg-red-600" />
          <Badge n={counts.WARNING ?? 0} cls="bg-amber-500" />
          <Badge n={counts.INFO ?? 0} cls="bg-blue-500" />
        </div>
      </div>

      {isLoading && <div className="text-sm text-slate-400">평가 중…</div>}
      {!isLoading && alerts.length === 0 && (
        <div className="text-sm text-green-600 bg-green-50 border border-green-200 rounded p-3">
          ✓ 감지된 경고가 없습니다.
        </div>
      )}

      {alerts.map((a, i) => (
        <AlertCard key={i} patientId={patientId} alert={a} acked={acked} onAck={onAck} />
      ))}
    </div>
  );
}

function Badge({ n, cls }: { n: number; cls: string }) {
  return <span className={`${cls} text-white rounded px-1.5 py-0.5 min-w-5 text-center`}>{n}</span>;
}

function alertKey(a: Alert) {
  return `${a.category}|${a.title}`;
}

function AlertCard({
  patientId,
  alert,
  acked,
  onAck,
}: {
  patientId: string;
  alert: Alert;
  acked: Set<string>;
  onAck: (key: string) => void;
}) {
  const style = SEVERITY_STYLE[alert.severity];
  const explain = useExplain();
  const [open, setOpen] = useState(false);
  const key = alertKey(alert);
  const isAcked = acked.has(key);

  const doExplain = () => {
    setOpen(true);
    if (!explain.data) explain.mutate({ patientId, alert });
  };

  return (
    <div className={`border rounded-lg p-3 ${style.bg} ${isAcked ? "opacity-60" : ""}`}>
      <div className="flex items-center gap-2 mb-1">
        <span className={`${style.dot} w-2 h-2 rounded-full`} />
        <span className={`text-xs font-bold ${style.text}`}>{style.label}</span>
        <span className="font-semibold text-sm">{alert.title}</span>
      </div>
      <p className="text-sm text-slate-700">{alert.description}</p>
      <p className="text-sm text-slate-600 mt-1">
        <span className="font-semibold">권고:</span> {alert.recommendation}
      </p>
      <p className="text-xs text-slate-400 mt-1">근거: {alert.evidence}</p>

      <div className="flex gap-2 mt-2">
        <button onClick={doExplain} className="text-xs px-2 py-1 bg-white border border-slate-300 rounded hover:bg-slate-50">
          자세히 (LLM 설명)
        </button>
        <button
          onClick={() => onAck(key)}
          disabled={isAcked}
          className="text-xs px-2 py-1 bg-white border border-slate-300 rounded hover:bg-slate-50 disabled:opacity-50"
        >
          {isAcked ? "확인됨 ✓" : "확인 (ack)"}
        </button>
      </div>

      {open && (
        <div className="mt-2 bg-white border border-slate-200 rounded p-2 text-sm">
          {explain.isPending && <span className="text-slate-400">설명 생성 중…</span>}
          {explain.data && (
            <>
              <p className="whitespace-pre-wrap text-slate-700">{explain.data.explanation}</p>
              <p className="text-xs text-amber-600 mt-2">{explain.data.disclaimer}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
