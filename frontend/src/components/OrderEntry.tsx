// 중앙 처방 입력: 약물 검색(자동완성) + 처방 장바구니 + 행별 인라인 경고 아이콘
import { useState } from "react";

import { useDrugSearch } from "../api/hooks";
import type { Alert, Severity } from "../lib/api";
import { usePrescription } from "../store/prescription";

const SEV_RANK: Record<Severity, number> = { CRITICAL: 0, WARNING: 1, INFO: 2 };

export default function OrderEntry({ alerts }: { alerts: Alert[] }) {
  const [query, setQuery] = useState("");
  const { data: results } = useDrugSearch(query);
  const { cart, addDrug, removeDrug, updateDose } = usePrescription();

  // 약물명 → 가장 높은 경고 등급 (행 인라인 아이콘용)
  const worstByDrug = new Map<string, Severity>();
  for (const a of alerts) {
    for (const d of a.related_drugs) {
      const cur = worstByDrug.get(d);
      if (!cur || SEV_RANK[a.severity] < SEV_RANK[cur]) worstByDrug.set(d, a.severity);
    }
  }
  const icon: Record<Severity, string> = { CRITICAL: "🔴", WARNING: "🟠", INFO: "🔵" };

  return (
    <div className="space-y-4">
      <div className="relative">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="약물 검색 (예: 와파린, ibuprofen)"
          className="w-full border border-slate-300 rounded px-3 py-2 text-sm"
        />
        {query && results && results.length > 0 && (
          <div className="absolute z-10 w-full bg-white border border-slate-200 rounded mt-1 max-h-64 overflow-auto shadow-lg">
            {results.map((d) => (
              <button
                key={d.code}
                onClick={() => {
                  addDrug(d);
                  setQuery("");
                }}
                className="w-full text-left px-3 py-2 text-sm hover:bg-slate-50 flex justify-between"
              >
                <span>
                  {d.name} <span className="text-slate-400 text-xs">{d.ingredient}</span>
                </span>
                <span className="text-slate-400 text-xs">{d.drug_class}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      <div>
        <div className="text-xs font-semibold text-slate-500 uppercase mb-2">처방 목록</div>
        {cart.length === 0 ? (
          <div className="text-sm text-slate-400 border border-dashed border-slate-300 rounded p-6 text-center">
            약물을 검색해 처방을 추가하세요.
          </div>
        ) : (
          <ul className="space-y-2">
            {cart.map((c) => {
              const sev = worstByDrug.get(c.name);
              return (
                <li key={c.drug_code} className="flex items-center gap-2 bg-white border border-slate-200 rounded px-3 py-2">
                  <span className="w-5 text-center" title={sev ?? ""}>{sev ? icon[sev] : ""}</span>
                  <span className="font-medium flex-1">{c.name}</span>
                  <input
                    value={c.dose ?? ""}
                    onChange={(e) => updateDose(c.drug_code, e.target.value)}
                    placeholder="용량·용법"
                    className="border border-slate-200 rounded px-2 py-1 text-sm w-40"
                  />
                  <span className="text-xs text-slate-400 w-10">{c.route}</span>
                  <button onClick={() => removeDrug(c.drug_code)} className="text-slate-400 hover:text-red-600 px-1">
                    ✕
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}
