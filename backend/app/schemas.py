from pydantic import BaseModel
from typing import List, Literal, Dict

class AgentStep(BaseModel):
    id: str
    name: str
    status: Literal["idle", "active", "completed"]
    subtext: str

class SecurityInsight(BaseModel):
    id: str
    title: str
    provider: Literal["AWS", "Azure", "GCP"]
    severity: Literal["Critical", "High", "Medium", "Low"]
    detected_at: str
    recommendation: str
    remediation_cli: str
    resolved: bool = False

class DashboardState(BaseModel):
    system_online: bool
    last_scan: str
    posture_score: int
    posture_delta: str
    critical_risks: int
    critical_delta: str
    resolved_today: int
    resolved_delta: str
    risk_distribution: Dict[str, int]
    threat_trends_7d: List[Dict[str, str | int]]
    provider_scores: Dict[str, int]
    key_metrics: Dict[str, str]
    agents: List[AgentStep]
    insights: List[SecurityInsight]