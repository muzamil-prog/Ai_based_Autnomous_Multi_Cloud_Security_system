from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.agents.pipeline import get_initial_dashboard_state

app = FastAPI(title="CloudSentinel AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory state for MVP (swap with SQLite/Postgres later)
STATE = get_initial_dashboard_state()

@app.get("/api/dashboard")
def get_dashboard():
    return STATE

@app.post("/api/remediate/{insight_id}")
def approve_remediation(insight_id: str):
    for item in STATE.insights:
        if item.id == insight_id:
            if item.resolved:
                return {"status": "already_resolved", "state": STATE}
            item.resolved = True
            STATE.resolved_today += 1
            if item.severity == "Critical" and STATE.critical_risks > 0:
                STATE.critical_risks -= 1
            STATE.posture_score = min(100, STATE.posture_score + 2)
            # Mark all agents completed after human approval
            for agent in STATE.agents:
                agent.status = "completed"
                if agent.id == "verify":
                    agent.subtext = "Fix verified!"
            return {"status": "remediated", "state": STATE}
    raise HTTPException(status_code=404, detail="Insight not found")