import React, { useEffect, useState } from "react";
import {
  Shield, Cloud, AlertTriangle, CheckCircle2, Search, BarChart3,
  Lightbulb, Wrench, ShieldCheck, ArrowRight, Sparkles, Zap, Clock,
  LayoutDashboard, Server, Activity, Bot, FileText, Settings
} from "lucide-react";
import {
  PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line,
  XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";

// 👇 PASTE YOUR PORT 8000 PUBLIC URL HERE (no trailing slash)
const API_BASE_URL = "https://solid-fishstick-97546x49pqrqcj4v-8000.app.github.dev";

interface AgentStep {
  id: string;
  name: string;
  status: "idle" | "active" | "completed";
  subtext: string;
}

interface SecurityInsight {
  id: string;
  title: string;
  provider: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  detected_at: string;
  recommendation: string;
  remediation_cli: string;
  resolved: boolean;
}

interface DashboardData {
  system_online: boolean;
  last_scan: string;
  posture_score: number;
  posture_delta: string;
  critical_risks: number;
  critical_delta: string;
  resolved_today: number;
  resolved_delta: string;
  risk_distribution: Record<string, number>;
  threat_trends_7d: { day: string; threats: number }[];
  provider_scores: Record<string, number>;
  key_metrics: { accuracy: string; response: string; avg_time: string; success_rate: string };
  agents: AgentStep[];
  insights: SecurityInsight[];
}

const DONUT_COLORS: Record<string, string> = {
  Low: "#10b981",
  Medium: "#f59e0b",
  High: "#ef4444",
  Critical: "#8b5cf6",
};

export default function App() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [selectedInsightId, setSelectedInsightId] = useState<string>("inc-1");
  const [approving, setApproving] = useState(false);

  const fetchDashboard = async () => {
    const res = await fetch(`${API_BASE_URL}/api/dashboard`);
    const json = await res.json();
    setData(json);
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleApproveFix = async (id: string) => {
    setApproving(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/remediate/${id}`, { method: "POST" });
      const json = await res.json();
      if (json.state) setData(json.state);
    } finally {
      setApproving(false);
    }
  };

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#050a18] text-cyan-400">
        Initializing CloudSentinel AI...
      </div>
    );
  }

  const donutData = Object.entries(data.risk_distribution).map(([name, value]) => ({ name, value }));
  const activeInsight = data.insights.find((i) => i.id === selectedInsightId) || data.insights[0];

  const getAgentIcon = (id: string) => {
    switch (id) {
      case "detection": return <Search className="w-5 h-5 text-cyan-400" />;
      case "analysis": return <BarChart3 className="w-5 h-5 text-cyan-400" />;
      case "explain": return <Lightbulb className="w-5 h-5 text-cyan-400" />;
      case "remediate": return <Wrench className="w-5 h-5 text-emerald-400" />;
      default: return <ShieldCheck className="w-5 h-5 text-emerald-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-[#050a18] text-slate-100 flex flex-col">
      {/* Top Navbar */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-cyan-950/60 bg-[#070e23]/90 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/40 shadow-[0_0_15px_rgba(6,182,212,0.3)]">
            <Shield className="w-7 h-7 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">CloudSentinel AI</h1>
            <p className="text-xs text-cyan-300/80">Autonomous. Explainable. Multi-Cloud Security.</p>
          </div>
        </div>

        <div className="flex items-center gap-6 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>System Online</span>
            <span className="text-slate-600">|</span>
            <span className="text-slate-400">Last Scan: {data.last_scan}</span>
          </div>
          <div className="px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-slate-200">
            Hello, Developer
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-56 border-r border-cyan-950/50 bg-[#060c1d] p-4 hidden md:flex flex-col gap-1.5 text-sm">
          {[
            { label: "Dashboard", icon: LayoutDashboard, active: true },
            { label: "Cloud Assets", icon: Server },
            { label: "Risk Analysis", icon: Activity },
            { label: "AI Agents", icon: Bot },
            { label: "Remediation", icon: Wrench },
            { label: "Reports", icon: FileText },
            { label: "Settings", icon: Settings },
          ].map((item) => (
            <button
              key={item.label}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-lg transition ${
                item.active
                  ? "bg-gradient-to-r from-cyan-600/30 to-blue-600/10 border border-cyan-500/40 text-white font-medium shadow-[0_0_12px_rgba(6,182,212,0.2)]"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50"
              }`}
            >
              <item.icon className="w-4 h-4 text-cyan-400" />
              {item.label}
            </button>
          ))}
        </aside>

        {/* Main Content Grid */}
        <main className="flex-1 p-6 space-y-5 overflow-y-auto">
          {/* Top Section: Cloud Hero + KPI Cards + Charts */}
          <div className="grid grid-cols-1 xl:grid-cols-12 gap-5">
            {/* Cloud Ecosystem Visual Banner */}
            <div className="xl:col-span-5 rounded-2xl border border-cyan-500/30 bg-gradient-to-b from-[#0b1938] to-[#071026] p-5 flex flex-col justify-between relative overflow-hidden">
              <div className="text-center z-10">
                <h2 className="text-sm font-semibold text-cyan-200 mb-4">
                  Unified Security Across Your Cloud Ecosystem
                </h2>
                <div className="flex justify-center gap-6 text-xs font-semibold">
                  <span className="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-amber-500/30 text-amber-400">AWS</span>
                  <span className="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-sky-500/30 text-sky-400">Microsoft Azure</span>
                  <span className="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-emerald-500/30 text-emerald-400">Google Cloud</span>
                </div>
              </div>

              <div className="my-6 flex flex-col items-center justify-center z-10">
                <div className="w-24 h-24 rounded-full bg-cyan-500/10 border-2 border-cyan-400/60 flex items-center justify-center shadow-[0_0_40px_rgba(34,211,238,0.35)]">
                  <Cloud className="w-12 h-12 text-cyan-300" />
                </div>
                <span className="mt-3 text-xs text-cyan-400/80">Real-Time Telemetry Synced</span>
              </div>
            </div>

            {/* Right 7 Columns: 3 KPIs + 2 Charts */}
            <div className="xl:col-span-7 space-y-5">
              {/* 3 KPI Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="rounded-2xl border border-emerald-500/30 bg-[#09152b] p-4">
                  <p className="text-xs text-slate-400">Overall Security Posture</p>
                  <div className="mt-3 flex items-center gap-3">
                    <ShieldCheck className="w-8 h-8 text-emerald-400" />
                    <span className="text-3xl font-bold">{data.posture_score}<span className="text-sm text-slate-400">/100</span></span>
                    <span className="text-xs text-emerald-400 font-semibold">{data.posture_delta}</span>
                  </div>
                </div>

                <div className="rounded-2xl border border-rose-500/30 bg-[#09152b] p-4">
                  <p className="text-xs text-slate-400">Critical Risks</p>
                  <div className="mt-3 flex items-center gap-3">
                    <AlertTriangle className="w-8 h-8 text-rose-500" />
                    <span className="text-3xl font-bold">{data.critical_risks}</span>
                    <span className="text-xs text-rose-400 font-semibold">{data.critical_delta}</span>
                  </div>
                </div>

                <div className="rounded-2xl border border-cyan-500/30 bg-[#09152b] p-4">
                  <p className="text-xs text-slate-400">Resolved Today</p>
                  <div className="mt-3 flex items-center gap-3">
                    <CheckCircle2 className="w-8 h-8 text-emerald-400" />
                    <span className="text-3xl font-bold">{data.resolved_today}</span>
                    <span className="text-xs text-emerald-400 font-semibold">{data.resolved_delta}</span>
                  </div>
                </div>
              </div>

              {/* Risk Distribution & 7-Day Threat Trends */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="rounded-2xl border border-slate-800 bg-[#09152b] p-4">
                  <h3 className="text-sm font-semibold mb-2">Risk Distribution</h3>
                  <div className="flex items-center">
                    <div className="w-36 h-36">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie data={donutData} dataKey="value" innerRadius={36} outerRadius={58} paddingAngle={2}>
                            {donutData.map((entry) => (
                              <Cell key={entry.name} fill={DONUT_COLORS[entry.name]} />
                            ))}
                          </Pie>
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="space-y-1.5 text-xs flex-1 pl-2">
                      {donutData.map((d) => (
                        <div key={d.name} className="flex justify-between">
                          <span className="flex items-center gap-2 text-slate-300">
                            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: DONUT_COLORS[d.name] }} />
                            {d.name}
                          </span>
                          <span className="font-semibold">{d.value}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-[#09152b] p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-sm font-semibold">Threat Trends (7 Days)</h3>
                    <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/20 text-emerald-400 font-semibold">↓ 60%</span>
                  </div>
                  <div className="h-36">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={data.threat_trends_7d}>
                        <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
                        <XAxis dataKey="day" stroke="#64748b" fontSize={10} />
                        <YAxis stroke="#64748b" fontSize={10} />
                        <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b" }} />
                        <Line type="monotone" dataKey="threats" stroke="#38bdf8" strokeWidth={2.5} dot={{ r: 3, fill: "#38bdf8" }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Middle Row: AI Security Agents Pipeline + Top Security Insights */}
          <div className="grid grid-cols-1 xl:grid-cols-12 gap-5">
            {/* 5-Agent Pipeline */}
            <div className="xl:col-span-8 rounded-2xl border border-cyan-500/30 bg-[#09152b] p-5">
              <div className="flex items-center gap-3 mb-4">
                <h3 className="text-base font-semibold">AI Security Agents at Work</h3>
                <span className="px-2 py-0.5 text-xs rounded-full bg-emerald-500/20 text-emerald-400 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" /> Live
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
                {data.agents.map((agent) => (
                  <div
                    key={agent.id}
                    className={`rounded-xl p-3.5 border text-center flex flex-col items-center justify-between transition ${
                      agent.status === "active"
                        ? "border-cyan-400 bg-cyan-950/40 shadow-[0_0_20px_rgba(34,211,238,0.2)]"
                        : agent.status === "completed"
                        ? "border-emerald-500/40 bg-[#0c1c38]"
                        : "border-slate-800 bg-[#071022] opacity-60"
                    }`}
                  >
                    <div className="p-2.5 rounded-full bg-slate-900 border border-slate-700 mb-2">
                      {getAgentIcon(agent.id)}
                    </div>
                    <p className="text-xs font-semibold text-white">{agent.name}</p>
                    <p className="text-[11px] text-cyan-300/80 mt-1">{agent.subtext}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Security Insights */}
            <div className="xl:col-span-4 rounded-2xl border border-slate-800 bg-[#09152b] p-5">
              <h3 className="text-base font-semibold mb-3">Top Security Insights</h3>
              <div className="space-y-2.5">
                {data.insights.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => setSelectedInsightId(item.id)}
                    className={`p-3 rounded-xl border cursor-pointer flex items-center justify-between transition ${
                      selectedInsightId === item.id
                        ? "border-cyan-400 bg-cyan-950/30"
                        : "border-slate-800 bg-[#060e1f] hover:border-slate-700"
                    }`}
                  >
                    <div>
                      <p className="text-xs font-medium text-white flex items-center gap-2">
                        {item.title}
                        {item.resolved && <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">Fixed</span>}
                      </p>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        Risk: <span className="text-amber-400">{item.severity}</span> • {item.detected_at}
                      </p>
                    </div>
                    <button className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300">
                      Review
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Bottom Row: Multi-Cloud Overview + Key Metrics + AI Recommendation */}
          <div className="grid grid-cols-1 xl:grid-cols-12 gap-5">
            {/* Multi-Cloud Scores */}
            <div className="xl:col-span-4 rounded-2xl border border-slate-800 bg-[#09152b] p-5">
              <h3 className="text-sm font-semibold mb-3">Multi-Cloud Security Overview</h3>
              <div className="space-y-2.5 text-xs">
                {Object.entries(data.provider_scores).map(([provider, score]) => (
                  <div key={provider} className="flex items-center justify-between p-2.5 rounded-lg bg-[#060e1f] border border-slate-800/80">
                    <span className="font-semibold text-slate-200">{provider}</span>
                    <span className="text-emerald-400 flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4" /> Secure ({score}/100)
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Key Metrics */}
            <div className="xl:col-span-4 rounded-2xl border border-slate-800 bg-[#09152b] p-5">
              <h3 className="text-sm font-semibold mb-3">Key Metrics</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center pt-2">
                <div>
                  <Shield className="w-5 h-5 text-cyan-400 mx-auto mb-1" />
                  <p className="text-lg font-bold">{data.key_metrics.accuracy}</p>
                  <p className="text-[11px] text-slate-400">Detection Accuracy</p>
                </div>
                <div>
                  <Zap className="w-5 h-5 text-amber-400 mx-auto mb-1" />
                  <p className="text-lg font-bold">{data.key_metrics.response}</p>
                  <p className="text-[11px] text-slate-400">Faster Response</p>
                </div>
                <div>
                  <Clock className="w-5 h-5 text-sky-400 mx-auto mb-1" />
                  <p className="text-lg font-bold">{data.key_metrics.avg_time}</p>
                  <p className="text-[11px] text-slate-400">Avg. Analysis Time</p>
                </div>
                <div>
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 mx-auto mb-1" />
                  <p className="text-lg font-bold">{data.key_metrics.success_rate}</p>
                  <p className="text-[11px] text-slate-400">Remediation Success</p>
                </div>
              </div>
            </div>

            {/* AI Recommendation & Human-in-the-Loop Approval */}
            <div className="xl:col-span-4 rounded-2xl border border-emerald-500/40 bg-gradient-to-br from-[#091e2c] to-[#081326] p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold mb-2">
                  <Sparkles className="w-4 h-4" /> AI Recommendation ({activeInsight.provider})
                </div>
                <p className="text-xs text-slate-200 leading-relaxed">{activeInsight.recommendation}</p>
                <code className="block mt-2 p-2 rounded bg-black/40 text-[10px] text-cyan-300 overflow-x-auto">
                  {activeInsight.remediation_cli}
                </code>
              </div>

              <button
                disabled={activeInsight.resolved || approving}
                onClick={() => handleApproveFix(activeInsight.id)}
                className="mt-4 w-full py-2.5 px-4 rounded-xl bg-emerald-400 hover:bg-emerald-300 disabled:bg-slate-700 disabled:text-slate-400 text-slate-950 font-semibold text-xs flex items-center justify-center gap-2 transition cursor-pointer"
              >
                {activeInsight.resolved ? (
                  <>
                    <CheckCircle2 className="w-4 h-4" /> Fix Applied & Verified
                  </>
                ) : (
                  <>
                    Apply Fix (with Approval) <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}