from app.schemas import DashboardData, AgentStep, SecurityInsight, CloudAsset, AuditReport

_state = DashboardData(
    system_online=True,
    last_scan="2 min ago",
    posture_score=92,
    posture_delta="+4%",
    critical_risks=2,
    critical_delta="-50%",
    resolved_today=24,
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
    agents=[
        AgentStep(id="detection", name="Detection Agent", status="active", subtext="Finding risks..."),
        AgentStep(id="analysis", name="Risk Analysis Agent", status="active", subtext="Prioritizing..."),
        AgentStep(id="explain", name="Explainability Agent", status="active", subtext="Explaining..."),
        AgentStep(id="remediate", name="Remediation Agent", status="completed", subtext="Planning actions..."),
        AgentStep(id="verify", name="Verification Agent", status="completed", subtext="Confirming..."),
    ],
    insights=[
        SecurityInsight(
            id="inc-1",
            title="Public S3 bucket detected in AWS",
            provider="AWS",
            severity="Critical",
            detected_at="2 min ago",
            recommendation="Block public access to sensitive data and enable encryption at rest.",
            remediation_cli="aws s3api put-public-access-block --bucket prod-sensitive-logs --public-access-block-configuration BlockPublicAcls=true",
            resolved=False,
        ),
        SecurityInsight(
            id="inc-2",
            title="Excessive permissions in Azure",
            provider="Azure",
            severity="Medium",
            detected_at="5 min ago",
            recommendation="Revoke wildcard Contributor role and assign least-privilege Reader access.",
            remediation_cli="az role assignment delete --assignee dev-svc-principal --role Contributor",
            resolved=False,
        ),
        SecurityInsight(
            id="inc-3",
            title="Unusual login pattern (GCP)",
            provider="GCP",
            severity="Low",
            detected_at="10 min ago",
            recommendation="Enforce MFA challenge and restrict session token lifetime on IAM account.",
            remediation_cli="gcloud iam service-accounts keys disable --iam-account=ops-bot@project.iam.gserviceaccount.com",
            resolved=False,
        ),
    ],
    assets=[
        CloudAsset(id="ast-1", name="prod-sensitive-logs", provider="AWS", service="S3 Storage", region="us-east-1", risk_level="Critical", status="Exposed"),
        CloudAsset(id="ast-2", name="core-eks-cluster-01", provider="AWS", service="Kubernetes (EKS)", region="us-west-2", risk_level="Low", status="Protected"),
        CloudAsset(id="ast-3", name="dev-svc-principal", provider="Azure", service="Entra IAM", region="eastus", risk_level="Medium", status="Over-privileged"),
        CloudAsset(id="ast-4", name="billing-sql-db", provider="Azure", service="Azure SQL", region="westeurope", risk_level="Low", status="Encrypted"),
        CloudAsset(id="ast-5", name="ops-bot-service-acct", provider="GCP", service="Cloud IAM", region="global", risk_level="Low", status="Monitored"),
        CloudAsset(id="ast-6", name="ml-training-vpc", provider="GCP", service="VPC Network", region="us-central1", risk_level="Low", status="Protected"),
    ],
    reports=[
        AuditReport(id="rep-104", timestamp="Today, 11:15 PM", framework="SOC 2 Type II + CIS Multi-Cloud", score="96% Compliant", findings_resolved=24, summary="Automated S3 public-access block and IAM privilege pruning verified across 3 cloud accounts."),
        AuditReport(id="rep-103", timestamp="Yesterday, 06:00 PM", framework="ISO 27001 Cloud Controls", score="93% Compliant", findings_resolved=18, summary="Zero unencrypted storage volumes detected; 2 stale service keys rotated."),
        AuditReport(id="rep-102", timestamp="Nov 25, 02:30 PM", framework="NIST CSF 2.0", score="91% Compliant", findings_resolved=15, summary="Network ingress rules tightened on staging Kubernetes clusters."),
    ],
)

def get_dashboard_state() -> DashboardData:
    return _state

def apply_remediation(insight_id: str) -> DashboardData:
    for item in _state.insights:
        if item.id == insight_id and not item.resolved:
            item.resolved = True
            if item.severity == "Critical" and _state.critical_risks > 0:
                _state.critical_risks -= 1
            _state.resolved_today += 1
            _state.posture_score = min(100, _state.posture_score + 2)
            _state.agents[3].status = "completed"
            _state.agents[3].subtext = "Action executed"
            _state.agents[4].status = "completed"
            _state.agents[4].subtext = "Fix verified!"
            if insight_id == "inc-1":
                _state.assets[0].risk_level = "Low"
                _state.assets[0].status = "Protected"
            elif insight_id == "inc-2":
                _state.assets[2].risk_level = "Low"
                _state.assets[2].status = "Protected"
    return _state
