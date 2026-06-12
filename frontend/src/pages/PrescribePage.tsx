// 처방 메인 화면 (CPOE): 좌(환자) · 중(처방입력) · 우(CDSS 경고) + 하단 서명
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { useEvaluate } from "../api/hooks";
import AlertPanel from "../components/AlertPanel";
import OrderEntry from "../components/OrderEntry";
import PatientPanel from "../components/PatientPanel";
import SignModal from "../components/SignModal";
import type { Alert } from "../lib/api";
import { usePrescription } from "../store/prescription";

export default function PrescribePage() {
  const { patientId, cart } = usePrescription();
  const [acked, setAcked] = useState<Set<string>>(new Set());
  const [showSign, setShowSign] = useState(false);
  const [signedMsg, setSignedMsg] = useState<string | null>(null);

  const orders = useMemo(
    () => cart.map((c) => ({ drug_code: c.drug_code, dose: c.dose, route: c.route })),
    [cart],
  );
  const { data, isFetching } = useEvaluate(patientId, orders);
  const alerts: Alert[] = data?.alerts ?? [];
  const counts = data?.counts ?? {};
  const hasCritical = data?.has_critical ?? false;

  if (!patientId) {
    return (
      <div className="p-8 text-center text-slate-500">
        선택된 환자가 없습니다. <Link to="/" className="text-blue-600 underline">환자 목록</Link>에서 선택하세요.
      </div>
    );
  }

  const toggleAck = (key: string) =>
    setAcked((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });

  const ackedAlerts = alerts.filter((a) => acked.has(`${a.category}|${a.title}`));

  return (
    <div className="grid grid-cols-12 gap-4 p-4">
      {/* 좌: 환자 패널 */}
      <aside className="col-span-3 bg-white border border-slate-200 rounded-lg p-4 h-fit sticky top-2">
        <PatientPanel patientId={patientId} />
      </aside>

      {/* 중: 처방 입력 */}
      <section className="col-span-5">
        <h1 className="text-lg font-bold mb-3">처방 입력 (CPOE)</h1>
        <OrderEntry alerts={alerts} />

        <div className="mt-4 flex items-center gap-3">
          <button
            onClick={() => setShowSign(true)}
            disabled={cart.length === 0}
            className={`px-4 py-2 rounded text-white font-semibold disabled:opacity-40 ${
              hasCritical ? "bg-red-600 hover:bg-red-700" : "bg-slate-900 hover:bg-black"
            }`}
          >
            처방 서명{hasCritical ? " (CRITICAL — 사유 필요)" : ""}
          </button>
          {signedMsg && <span className="text-sm text-green-600">✓ {signedMsg}</span>}
        </div>
      </section>

      {/* 우: CDSS 경고 패널 */}
      <aside className="col-span-4 bg-white border border-slate-200 rounded-lg p-4 h-fit sticky top-2">
        <AlertPanel
          patientId={patientId}
          alerts={alerts}
          counts={counts}
          isLoading={isFetching}
          acked={acked}
          onAck={toggleAck}
        />
      </aside>

      {showSign && (
        <SignModal
          patientId={patientId}
          orders={orders}
          hasCritical={hasCritical}
          acked={ackedAlerts}
          onClose={() => setShowSign(false)}
          onSigned={(msg) => {
            setSignedMsg(msg);
            setShowSign(false);
          }}
        />
      )}
    </div>
  );
}
