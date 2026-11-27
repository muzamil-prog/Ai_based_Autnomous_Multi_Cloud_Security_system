import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.agents.pipeline import get_dashboard_state, apply_remediation, record_completed_scan

app = FastAPI(title="CloudSentinel AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard")
def read_dashboard():
    return get_dashboard_state()

@app.post("/api/remediate/{insight_id}")
def remediate_issue(insight_id: str):
    updated_state = apply_remediation(insight_id)
    return {"status": "success", "state": updated_state}

@app.get("/api/scan/stream")
async def stream_scan():
    async def event_generator():
        stages = [
            ("detection", "Scanning AWS, Azure & GCP assets..."),
            ("analysis", "Scoring CVE & IAM blast radius..."),
            ("explain", "Generating plain-English risk context..."),
            ("remediate", "Synthesizing least-privilege CLI fixes..."),
            ("verify", "Validating policy compliance & drift..."),
        ]

        state = get_dashboard_state().model_dump()
        for agent in state["agents"]:
            agent["status"] = "idle"
            agent["subtext"] = "Waiting..."
        yield f"data: {json.dumps(state)}\n\n"
        await asyncio.sleep(0.5)

        for idx, (agent_id, active_msg) in enumerate(stages):
            state["agents"][idx]["status"] = "active"
            state["agents"][idx]["subtext"] = active_msg
            yield f"data: {json.dumps(state)}\n\n"
            await asyncio.sleep(1.1)

            state["agents"][idx]["status"] = "completed"
            state["agents"][idx]["subtext"] = "Completed"

        final_state = record_completed_scan().model_dump()
        for agent in final_state["agents"]:
            agent["status"] = "completed"
            agent["subtext"] = "Completed"
        yield f"data: {json.dumps(final_state)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
