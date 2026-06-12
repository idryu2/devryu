// 백엔드 API 클라이언트 + 타입 (OpenAPI 스키마와 일치)

const BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type Severity = "CRITICAL" | "WARNING" | "INFO";

export interface PatientSummary {
  id: string;
  name: string;
  age: number;
  sex: string;
  encounter_type: string;
  ward: string | null;
  bed: string | null;
}

export interface Allergy {
  substance: string;
  reaction: string | null;
  severity: string | null;
}
export interface Condition {
  code: string;
  display: string;
}
export interface Lab {
  code: string;
  display: string;
  value: number;
  unit: string | null;
  abnormal: boolean;
  ref_low: number | null;
  ref_high: number | null;
}
export interface Medication {
  drug_code: string;
  dose: string | null;
}

export interface PatientDetail extends PatientSummary {
  weight_kg: number;
  egfr: number | null;
  creatinine: number | null;
  pregnant: boolean;
  allergies: Allergy[];
  conditions: Condition[];
  labs: Lab[];
  medications: Medication[];
}

export interface Drug {
  code: string;
  name: string;
  ingredient: string;
  drug_class: string;
  default_dose: string | null;
  route: string | null;
  renal_adjust: boolean;
  pregnancy_category: string | null;
  beers: boolean;
  flags: string[];
}

export interface OrderIn {
  drug_code: string;
  dose?: string | null;
  route?: string | null;
}

export interface Alert {
  severity: Severity;
  category: string;
  title: string;
  description: string;
  recommendation: string;
  evidence: string;
  related_drugs: string[];
}

export interface EvaluateResponse {
  patient_id: string;
  alerts: Alert[];
  counts: Record<string, number>;
  has_critical: boolean;
}

export interface AskResponse {
  answer: string;
  sources: { doc_title: string; section: string; source_label: string }[];
  disclaimer: string;
}

export interface AuditEntry {
  id: number;
  ts: string;
  patient_id: string | null;
  actor: string;
  action: string;
  detail: Record<string, unknown>;
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "content-type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export const api = {
  listPatients: () => req<PatientSummary[]>("/patients"),
  getPatient: (id: string) => req<PatientDetail>(`/patients/${id}`),
  searchDrugs: (query: string) =>
    req<Drug[]>(`/drugs?query=${encodeURIComponent(query)}`),
  evaluate: (patient_id: string, orders: OrderIn[]) =>
    req<EvaluateResponse>("/cdss/evaluate", {
      method: "POST",
      body: JSON.stringify({ patient_id, orders }),
    }),
  explain: (patient_id: string, alert: Alert) =>
    req<{ explanation: string; disclaimer: string }>("/cdss/explain", {
      method: "POST",
      body: JSON.stringify({ patient_id, alert }),
    }),
  ask: (question: string) =>
    req<AskResponse>("/guidelines/ask", {
      method: "POST",
      body: JSON.stringify({ question }),
    }),
  sign: (body: {
    patient_id: string;
    orders: OrderIn[];
    override_reason?: string | null;
    acknowledged_alerts?: Alert[];
  }) =>
    req<{ signed: boolean; audit_id: number; overridden: boolean; message: string }>(
      "/orders/sign",
      { method: "POST", body: JSON.stringify(body) },
    ),
  audit: () => req<AuditEntry[]>("/audit"),
};

export const SEVERITY_STYLE: Record<Severity, { bg: string; text: string; label: string; dot: string }> = {
  CRITICAL: { bg: "bg-red-50 border-red-300", text: "text-red-700", label: "위험", dot: "bg-red-600" },
  WARNING: { bg: "bg-amber-50 border-amber-300", text: "text-amber-700", label: "경고", dot: "bg-amber-500" },
  INFO: { bg: "bg-blue-50 border-blue-300", text: "text-blue-700", label: "정보", dot: "bg-blue-500" },
};
