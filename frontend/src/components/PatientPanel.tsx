// 좌측 환자 핵심 정보 패널: 인구학 · 알레르기(빨강) · 복용약 · 검사(비정상 강조) · 진단
import { usePatient } from "../api/hooks";

export default function PatientPanel({ patientId }: { patientId: string }) {
  const { data: p, isLoading } = usePatient(patientId);

  if (isLoading || !p) return <div className="p-4 text-sm text-slate-500">환자 정보 불러오는 중…</div>;

  return (
    <div className="space-y-4 text-sm">
      <div>
        <div className="text-lg font-bold">
          {p.name} <span className="text-slate-400 text-xs">{p.id}</span>
        </div>
        <div className="text-slate-500">
          {p.age}세 · {p.sex === "M" ? "남" : "여"} · {p.weight_kg}kg ·{" "}
          {p.encounter_type === "inpatient" ? `입원 ${p.ward ?? ""} ${p.bed ?? ""}` : "외래"}
          {p.pregnant && <span className="ml-1 px-1.5 py-0.5 bg-pink-100 text-pink-700 rounded text-xs">임신</span>}
        </div>
      </div>

      <Field label="신기능">
        eGFR {p.egfr ?? "N/A"} mL/min/1.73㎡ {p.creatinine ? `· Cr ${p.creatinine}` : ""}
      </Field>

      <div>
        <Label>알레르기</Label>
        {p.allergies.length === 0 ? (
          <div className="text-slate-400">없음</div>
        ) : (
          <div className="flex flex-wrap gap-1">
            {p.allergies.map((a) => (
              <span key={a.substance} className="px-2 py-0.5 bg-red-100 text-red-700 font-semibold rounded">
                ⚠ {a.substance}
              </span>
            ))}
          </div>
        )}
      </div>

      <div>
        <Label>진단</Label>
        <div className="flex flex-wrap gap-1">
          {p.conditions.map((c) => (
            <span key={c.code} className="px-2 py-0.5 bg-slate-100 rounded">
              {c.display}
            </span>
          ))}
        </div>
      </div>

      <div>
        <Label>현재 복용약</Label>
        {p.medications.length === 0 ? (
          <div className="text-slate-400">없음</div>
        ) : (
          <ul className="list-disc list-inside text-slate-700">
            {p.medications.map((m) => (
              <li key={m.drug_code}>{m.drug_code}{m.dose ? ` (${m.dose})` : ""}</li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <Label>주요 검사</Label>
        {p.labs.length === 0 ? (
          <div className="text-slate-400">없음</div>
        ) : (
          <table className="w-full">
            <tbody>
              {p.labs.map((l) => (
                <tr key={l.code} className={l.abnormal ? "text-red-600 font-semibold" : ""}>
                  <td className="py-0.5">{l.display}</td>
                  <td className="py-0.5 text-right">
                    {l.value} {l.unit} {l.abnormal && "▲"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

const Label = ({ children }: { children: React.ReactNode }) => (
  <div className="text-xs font-semibold text-slate-500 uppercase mb-1">{children}</div>
);
const Field = ({ label, children }: { label: string; children: React.ReactNode }) => (
  <div>
    <Label>{label}</Label>
    <div>{children}</div>
  </div>
);
