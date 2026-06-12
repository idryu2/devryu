import { NavLink, Route, Routes } from "react-router-dom";

import DemoBanner from "./components/DemoBanner";
import AuditPage from "./pages/AuditPage";
import DashboardPage from "./pages/DashboardPage";
import GuidelineQAPage from "./pages/GuidelineQAPage";
import PatientListPage from "./pages/PatientListPage";
import PrescribePage from "./pages/PrescribePage";

const navItems = [
  { to: "/", label: "환자 목록", end: true },
  { to: "/prescribe", label: "처방(CPOE)" },
  { to: "/guidelines", label: "가이드라인 Q&A" },
  { to: "/audit", label: "감사 로그" },
  { to: "/dashboard", label: "경고 통계" },
];

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <DemoBanner />
      <header className="bg-slate-900 text-white px-4 py-2 flex items-center gap-6">
        <span className="font-bold text-lg">처방 CDSS</span>
        <nav className="flex gap-1 text-sm">
          {navItems.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              className={({ isActive }) =>
                `px-3 py-1.5 rounded ${isActive ? "bg-slate-700" : "hover:bg-slate-800"}`
              }
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<PatientListPage />} />
          <Route path="/prescribe" element={<PrescribePage />} />
          <Route path="/guidelines" element={<GuidelineQAPage />} />
          <Route path="/audit" element={<AuditPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>
    </div>
  );
}
