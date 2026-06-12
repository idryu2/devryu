// 처방 서명 모달: CRITICAL 경고가 있으면 override 사유 입력을 강제
import { useState } from "react";

import { useSign } from "../api/hooks";
import type { Alert } from "../lib/api";

export interface CartItemSign {
  drug_code: string;
  dose?: string | null;
  route?: string | null;
}

export default function SignModal({
  patientId,
  orders,
  hasCritical,
  acked,
  onClose,
  onSigned,
}: {
  patientId: string;
  orders: CartItemSign[];
  hasCritical: boolean;
  acked: Alert[];
  onClose: () => void;
  onSigned: (msg: string) => void;
}) {
  const [reason, setReason] = useState("");
  const sign = useSign();

  const submit = () => {
    sign.mutate(
      {
        patient_id: patientId,
        orders: orders.map((o) => ({ drug_code: o.drug_code, dose: o.dose, route: o.route })),
        override_reason: hasCritical ? reason : null,
        acknowledged_alerts: acked,
      },
      {
        onSuccess: (res) => onSigned(res.message),
        onError: () => {
          /* 에러는 아래 표시 */
        },
      },
    );
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-5 w-[480px] max-w-[90vw]">
        <h3 className="font-bold text-lg mb-2">처방 서명</h3>

        {hasCritical ? (
          <div className="bg-red-50 border border-red-300 rounded p-3 text-sm text-red-700 mb-3">
            ⚠ CRITICAL 경고가 있습니다. 처방을 강행하려면 <b>override 사유</b>를 입력해야 하며,
            이 결정은 감사 로그에 기록됩니다.
          </div>
        ) : (
          <p className="text-sm text-slate-600 mb-3">아래 처방 {orders.length}건을 서명합니다.</p>
        )}

        {hasCritical && (
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="override 사유를 입력하세요 (필수)"
            className="w-full border border-slate-300 rounded p-2 text-sm h-24 mb-2"
          />
        )}

        {sign.isError && <p className="text-sm text-red-600 mb-2">{String((sign.error as Error).message)}</p>}

        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1.5 text-sm border border-slate-300 rounded">
            취소
          </button>
          <button
            onClick={submit}
            disabled={(hasCritical && !reason.trim()) || sign.isPending}
            className="px-3 py-1.5 text-sm bg-slate-900 text-white rounded disabled:opacity-50"
          >
            {sign.isPending ? "서명 중…" : hasCritical ? "사유와 함께 서명" : "서명"}
          </button>
        </div>
      </div>
    </div>
  );
}
