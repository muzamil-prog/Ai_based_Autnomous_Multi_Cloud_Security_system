from pydantic import BaseModel
from typing import List, Dict

class AgentStep(BaseModel):
    id: str
    name: str
    status: str  # "idle" | "active" | "completed"
    subtext: str

class SecurityInsight(BaseModel):
    id: str
    title: str
    provider: str
    severity: str
    detected_at: str
    recommendation: str
    remediation_cli: str
    resolved: bool = False

class DashboardData(BaseModel):
    system_online: bool
    last_scan: str
    posture_score: int
    posture_delta: str
    critical_risks: int
    critical_delta: str
    resolved_today: int
    resolved_delta: str
    risk_distribution: Dict[str, int]
    threat_trends_7d: List[Dict[str, object]]
    provider_scores: Dict[str, int]
    key_metrics: Dict[str, str]
    agents: List[AgentStep]
    insights: List[SecurityInsight]
