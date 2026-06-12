import { useNavigate } from "react-router-dom";

import { usePatients } from "../api/hooks";
import { usePrescription } from "../store/prescription";

export default function PatientListPage() {
  const { data: patients, isLoading, error } = usePatients();
  const setPatient = usePrescription((s) => s.setPatient);
  const navigate = useNavigate();

  const select = (id: string) => {
    setPatient(id);
    navigate("/prescribe");
  };

  const inpatients = patients?.filter((p) => p.encounter_type === "inpatient") ?? [];
  const outpatients = patients?.filter((p) => p.encounter_type === "outpatient") ?? [];

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-xl font-bold mb-1">환자 목록</h1>
      <p className="text-sm text-slate-500 mb-4">처방할 환자를 선택하면 CPOE 화면으로 이동합니다.</p>

      {isLoading && <p>불러오는 중…</p>}
      {error && <p className="text-red-600">백엔드 연결 실패: {String((error as Error).message)}</p>}

      <Section title="입원 환자" items={inpatients} onSelect={select} />
      <Section title="외래 환자" items={outpatients} onSelect={select} />
    </div>
  );
}

function Section({
  title,
  items,
  onSelect,
}: {
  title: string;
  items: { id: string; name: string; age: number; sex: string; ward: string | null; bed: string | null }[];
  onSelect: (id: string) => void;
}) {
  if (items.length === 0) return null;
  return (
    <div className="mb-6">
      <h2 className="text-sm font-semibold text-slate-600 mb-2">{title}</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {items.map((p) => (
          <button
            key={p.id}
            onClick={() => onSelect(p.id)}
            className="text-left bg-white border border-slate-200 rounded-lg p-3 hover:border-slate-400 hover:shadow-sm transition"
          >
            <div className="font-semibold">
              {p.name} <span className="text-slate-400 text-xs">{p.id}</span>
            </div>
            <div className="text-sm text-slate-500">
              {p.age}세 · {p.sex === "M" ? "남" : "여"}
              {p.ward ? ` · ${p.ward} ${p.bed ?? ""}` : ""}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
