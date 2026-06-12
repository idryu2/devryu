// (선택) 경고 통계: 감사 로그 기반 등급 분포 / override 비율 — 경고 적정성 시연
import { useAudit } from "../api/hooks";
import type { Alert } from "../lib/api";

export default function DashboardPage() {
  const { data } = useAudit();
  const logs = data ?? [];

  const total = logs.length;
  const overrides = logs.filter((l) => l.action === "override").length;
  const overrideRate = total ? Math.round((overrides / total) * 100) : 0;

  // 서명 시 평가된 경고들의 등급 분포 집계
  const sev = { CRITICAL: 0, WARNING: 0, INFO: 0 } as Record<string, number>;
  const cat: Record<string, number> = {};
  for (const l of logs) {
    const alerts = ((l.detail as { alerts?: Alert[] }).alerts ?? []) as Alert[];
    for (const a of alerts) {
      sev[a.severity] = (sev[a.severity] ?? 0) + 1;
      cat[a.category] = (cat[a.category] ?? 0) + 1;
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-xl font-bold mb-4">경고 통계 대시보드</h1>
      <p className="text-sm text-slate-500 mb-4">
        감사 로그에 기록된 서명 이벤트 기준 집계 (경고 피로/적정성 분석 관점 시연).
      </p>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <Stat label="총 서명 이벤트" value={String(total)} />
        <Stat label="Override 건수" value={String(overrides)} />
        <Stat label="Override 비율" value={`${overrideRate}%`} />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-lg p-4">
          <h2 className="font-semibold mb-3 text-sm">등급별 경고 분포</h2>
          <Bar label="CRITICAL" n={sev.CRITICAL} max={Math.max(1, ...Object.values(sev))} cls="bg-red-600" />
          <Bar label="WARNING" n={sev.WARNING} max={Math.max(1, ...Object.values(sev))} cls="bg-amber-500" />
          <Bar label="INFO" n={sev.INFO} max={Math.max(1, ...Object.values(sev))} cls="bg-blue-500" />
        </div>
        <div className="bg-white border border-slate-200 rounded-lg p-4">
          <h2 className="font-semibold mb-3 text-sm">카테고리별 경고</h2>
          {Object.keys(cat).length === 0 && <p className="text-sm text-slate-400">데이터 없음</p>}
          {Object.entries(cat)
            .sort((a, b) => b[1] - a[1])
            .map(([k, v]) => (
              <Bar key={k} label={k} n={v} max={Math.max(1, ...Object.values(cat))} cls="bg-slate-600" />
            ))}
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-4 text-center">
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs text-slate-500 mt-1">{label}</div>
    </div>
  );
}

function Bar({ label, n, max, cls }: { label: string; n: number; max: number; cls: string }) {
  return (
    <div className="flex items-center gap-2 mb-2 text-xs">
      <span className="w-24 truncate">{label}</span>
      <div className="flex-1 bg-slate-100 rounded h-4">
        <div className={`${cls} h-4 rounded`} style={{ width: `${(n / max) * 100}%` }} />
      </div>
      <span className="w-6 text-right">{n}</span>
    </div>
  );
}
