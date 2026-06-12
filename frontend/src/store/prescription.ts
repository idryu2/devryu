// 처방 화면 상태: 선택 환자 + 처방 장바구니 (Zustand)
import { create } from "zustand";

import type { Drug, OrderIn } from "../lib/api";

export interface CartItem extends OrderIn {
  name: string;
}

interface PrescriptionState {
  patientId: string | null;
  cart: CartItem[];
  setPatient: (id: string) => void;
  addDrug: (drug: Drug) => void;
  removeDrug: (drugCode: string) => void;
  updateDose: (drugCode: string, dose: string) => void;
  clearCart: () => void;
}

export const usePrescription = create<PrescriptionState>((set) => ({
  patientId: null,
  cart: [],
  setPatient: (id) => set({ patientId: id, cart: [] }),
  addDrug: (drug) =>
    set((s) =>
      s.cart.some((c) => c.drug_code === drug.code)
        ? s
        : {
            cart: [
              ...s.cart,
              { drug_code: drug.code, name: drug.name, dose: drug.default_dose, route: drug.route },
            ],
          },
    ),
  removeDrug: (code) => set((s) => ({ cart: s.cart.filter((c) => c.drug_code !== code) })),
  updateDose: (code, dose) =>
    set((s) => ({ cart: s.cart.map((c) => (c.drug_code === code ? { ...c, dose } : c)) })),
  clearCart: () => set({ cart: [] }),
}));
