// 감사 로그: 처방 서명 / override 사유 / 경고 확인 이력 (CDSS 거버넌스)
import { useAudit } from "../api/hooks";

export default function AuditPage() {
  const { data, isLoading } = useAudit();

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-xl font-bold mb-4">감사 로그</h1>
      {isLoading && <p>불러오는 중…</p>}
      {data && data.length === 0 && <p className="text-slate-400">기록이 없습니다.</p>}

      <div className="space-y-2">
        {data?.map((e) => {
          const reason = (e.detail as { override_reason?: string }).override_reason;
          const orders = (e.detail as { orders?: { drug_code: string }[] }).orders ?? [];
          return (
            <div key={e.id} className="bg-white border border-slate-200 rounded-lg p-3 text-sm">
              <div className="flex items-center gap-2">
                <span
                  className={`px-2 py-0.5 rounded text-xs font-semibold ${
                    e.action === "override" ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
                  }`}
                >
                  {e.action === "override" ? "OVERRIDE" : "서명"}
                </span>
                <span className="font-semibold">{e.patient_id}</span>
                <span className="text-slate-400 text-xs">{new Date(e.ts).toLocaleString("ko-KR")}</span>
                <span className="text-slate-400 text-xs ml-auto">{e.actor}</span>
              </div>
              <div className="text-slate-600 mt-1">
                처방: {orders.map((o) => o.drug_code).join(", ") || "—"}
              </div>
              {reason && (
                <div className="text-red-600 mt-1">
                  <b>override 사유:</b> {reason}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
