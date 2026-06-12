// TanStack Query 훅
import { keepPreviousData, useMutation, useQuery } from "@tanstack/react-query";

import { api, type Alert, type OrderIn } from "../lib/api";

export const usePatients = () =>
  useQuery({ queryKey: ["patients"], queryFn: api.listPatients });

export const usePatient = (id: string | null) =>
  useQuery({
    queryKey: ["patient", id],
    queryFn: () => api.getPatient(id as string),
    enabled: !!id,
  });

export const useDrugSearch = (query: string) =>
  useQuery({
    queryKey: ["drugs", query],
    queryFn: () => api.searchDrugs(query),
    enabled: query.length >= 1,
    placeholderData: keepPreviousData,
  });

// 처방이 바뀔 때마다 실시간 재평가 (CDSS 핵심)
export const useEvaluate = (patientId: string | null, orders: OrderIn[]) =>
  useQuery({
    queryKey: ["evaluate", patientId, orders],
    queryFn: () => api.evaluate(patientId as string, orders),
    enabled: !!patientId,
  });

export const useExplain = () =>
  useMutation({
    mutationFn: ({ patientId, alert }: { patientId: string; alert: Alert }) =>
      api.explain(patientId, alert),
  });

export const useAsk = () =>
  useMutation({ mutationFn: (question: string) => api.ask(question) });

export const useSign = () => useMutation({ mutationFn: api.sign });

export const useAudit = () =>
  useQuery({ queryKey: ["audit"], queryFn: api.audit });
