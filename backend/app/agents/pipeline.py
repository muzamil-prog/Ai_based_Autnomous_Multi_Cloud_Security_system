from datetime import datetime
from app.schemas import DashboardData, AgentStep, SecurityInsight, CloudAsset, AuditReport
from app.database import init_db, get_conn

init_db()

_agents: list[AgentStep] = [
    AgentStep(id="detection", name="Detection Agent", status="active", subtext="Finding risks..."),
    AgentStep(id="analysis", name="Risk Analysis Agent", status="active", subtext="Prioritizing..."),
    AgentStep(id="explain", name="Explainability Agent", status="active", subtext="Explaining..."),
    AgentStep(id="remediate", name="Remediation Agent", status="completed", subtext="Planning actions..."),
    AgentStep(id="verify", name="Verification Agent", status="completed", subtext="Confirming..."),
]

def get_dashboard_state() -> DashboardData:
    with get_conn() as conn:
        m = conn.execute("SELECT * FROM metrics WHERE id = 1").fetchone()
        insight_rows = conn.execute("SELECT * FROM insights").fetchall()
        asset_rows = conn.execute("SELECT * FROM assets").fetchall()
        report_rows = conn.execute("SELECT * FROM reports ORDER BY rowid DESC").fetchall()

    insights = [
        SecurityInsight(
            id=r["id"], title=r["title"], provider=r["provider"], severity=r["severity"],
            detected_at=r["detected_at"], recommendation=r["recommendation"],
            remediation_cli=r["remediation_cli"], resolved=bool(r["resolved"])
        ) for r in insight_rows
    ]
    assets = [
        CloudAsset(
            id=r["id"], name=r["name"], provider=r["provider"], service=r["service"],
            region=r["region"], risk_level=r["risk_level"], status=r["status"]
        ) for r in asset_rows
    ]
    reports = [
        AuditReport(
            id=r["id"], timestamp=r["timestamp"], framework=r["framework"],
            score=r["score"], findings_resolved=r["findings_resolved"], summary=r["summary"]
        ) for r in report_rows
    ]

    return DashboardData(
        system_online=True,
        last_scan=m["last_scan"],
        posture_score=m["posture_score"],
        posture_delta="+4%",
        critical_risks=m["critical_risks"],
        critical_delta="-50%",
        resolved_today=m["resolved_today"],
        resolved_delta="+20%",
        risk_distribution={"Low": 62, "Medium": 25, "High": 9, "Critical": 4},
        threat_trends_7d=[
            {"day": "Mon", "threats": 72},
            {"day": "Tue", "threats": 85},
            {"day": "Wed", "threats": 79},
            {"day": "Thu", "threats": 64},
            {"day": "Fri", "threats": 61},
            {"day": "Sat", "threats": 45},
            {"day": "Sun", "threats": 28},
        ],
        provider_scores={"AWS": 96, "Azure": 94, "GCP": 92},
        key_metrics={
            "accuracy": "99.8%",
            "response": "38%",
            "avg_time": "2.4 min",
            "success_rate": "97%",
        },
        agents=_agents,
        insights=insights,
        assets=assets,
        reports=reports,
    )

def apply_remediation(insight_id: str) -> DashboardData:
    with get_conn() as conn:
        ins = conn.execute("SELECT * FROM insights WHERE id = ?", (insight_id,)).fetchone()
        if ins and not ins["resolved"]:
            conn.execute("UPDATE insights SET resolved = 1 WHERE id = ?", (insight_id,))
            m = conn.execute("SELECT * FROM metrics WHERE id = 1").fetchone()
            new_critical = max(0, m["critical_risks"] - 1) if ins["severity"] == "Critical" else m["critical_risks"]
            new_resolved = m["resolved_today"] + 1
            new_score = min(100, m["posture_score"] + 2)
            conn.execute(
                "UPDATE metrics SET critical_risks = ?, resolved_today = ?, posture_score = ? WHERE id = 1",
                (new_critical, new_resolved, new_score),
            )
            if insight_id == "inc-1":
                conn.execute("UPDATE assets SET risk_level = 'Low', status = 'Protected' WHERE id = 'ast-1'")
            elif insight_id == "inc-2":
                conn.execute("UPDATE assets SET risk_level = 'Low', status = 'Protected' WHERE id = 'ast-3'")

            rep_id = f"rep-{105 + new_resolved}"
            now_str = datetime.now().strftime("Today, %I:%M %p")
            conn.execute(
                "INSERT OR REPLACE INTO reports VALUES (?, ?, ?, ?, ?, ?)",
                (rep_id, now_str, f"{ins['provider']} Autonomous Remediation", f"{new_score}% Compliant",
                 new_resolved, f"Human-approved fix applied and verified for: {ins['title']}."),
            )

            _agents[3].status = "completed"
            _agents[3].subtext = "Action executed"
            _agents[4].status = "completed"
            _agents[4].subtext = "Fix verified!"

    return get_dashboard_state()

def record_completed_scan() -> DashboardData:
    now_str = datetime.now().strftime("Today, %I:%M %p")
    with get_conn() as conn:
        conn.execute("UPDATE metrics SET last_scan = ? WHERE id = 1", (now_str,))
        m = conn.execute("SELECT * FROM metrics WHERE id = 1").fetchone()
        count = conn.execute("SELECT COUNT(*) as c FROM reports").fetchone()["c"]
        conn.execute(
            "INSERT INTO reports VALUES (?, ?, ?, ?, ?, ?)",
            (f"rep-{105 + count}", now_str, "Multi-Cloud Full Telemetry Scan", f"{m['posture_score']}% Compliant",
             m["resolved_today"], "Completed 5-agent autonomous scan across AWS, Azure, and GCP assets."),
        )
    return get_dashboard_state()
