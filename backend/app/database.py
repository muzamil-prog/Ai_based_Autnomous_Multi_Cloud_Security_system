import sqlite3
from pathlib import Path
from typing import List
from app.schemas import DashboardData, AgentStep, SecurityInsight, CloudAsset, AuditReport

DB_PATH = Path(__file__).resolve().parent.parent / "cloudsentinel.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                last_scan TEXT NOT NULL,
                posture_score INTEGER NOT NULL,
                critical_risks INTEGER NOT NULL,
                resolved_today INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS insights (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                provider TEXT NOT NULL,
                severity TEXT NOT NULL,
                detected_at TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                remediation_cli TEXT NOT NULL,
                resolved INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS assets (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                provider TEXT NOT NULL,
                service TEXT NOT NULL,
                region TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                framework TEXT NOT NULL,
                score TEXT NOT NULL,
                findings_resolved INTEGER NOT NULL,
                summary TEXT NOT NULL
            );
        """)

        row = conn.execute("SELECT id FROM metrics WHERE id = 1").fetchone()
        if not row:
            conn.execute(
                "INSERT INTO metrics (id, last_scan, posture_score, critical_risks, resolved_today) VALUES (1, ?, ?, ?, ?)",
                ("2 min ago", 92, 2, 24),
            )
            conn.executemany(
                "INSERT INTO insights VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    ("inc-1", "Public S3 bucket detected in AWS", "AWS", "Critical", "2 min ago",
                     "Block public access to sensitive data and enable encryption at rest.",
                     "aws s3api put-public-access-block --bucket prod-sensitive-logs --public-access-block-configuration BlockPublicAcls=true", 0),
                    ("inc-2", "Excessive permissions in Azure", "Azure", "Medium", "5 min ago",
                     "Revoke wildcard Contributor role and assign least-privilege Reader access.",
                     "az role assignment delete --assignee dev-svc-principal --role Contributor", 0),
                    ("inc-3", "Unusual login pattern (GCP)", "GCP", "Low", "10 min ago",
                     "Enforce MFA challenge and restrict session token lifetime on IAM account.",
                     "gcloud iam service-accounts keys disable --iam-account=ops-bot@project.iam.gserviceaccount.com", 0),
                ],
            )
            conn.executemany(
                "INSERT INTO assets VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    ("ast-1", "prod-sensitive-logs", "AWS", "S3 Storage", "us-east-1", "Critical", "Exposed"),
                    ("ast-2", "core-eks-cluster-01", "AWS", "Kubernetes (EKS)", "us-west-2", "Low", "Protected"),
                    ("ast-3", "dev-svc-principal", "Azure", "Entra IAM", "eastus", "Medium", "Over-privileged"),
                    ("ast-4", "billing-sql-db", "Azure", "Azure SQL", "westeurope", "Low", "Encrypted"),
                    ("ast-5", "ops-bot-service-acct", "GCP", "Cloud IAM", "global", "Low", "Monitored"),
                    ("ast-6", "ml-training-vpc", "GCP", "VPC Network", "us-central1", "Low", "Protected"),
                ],
            )
            conn.executemany(
                "INSERT INTO reports VALUES (?, ?, ?, ?, ?, ?)",
                [
                    ("rep-104", "Today, 11:15 PM", "SOC 2 Type II + CIS Multi-Cloud", "96% Compliant", 24,
                     "Automated S3 public-access block and IAM privilege pruning verified across 3 cloud accounts."),
                    ("rep-103", "Yesterday, 06:00 PM", "ISO 27001 Cloud Controls", "93% Compliant", 18,
                     "Zero unencrypted storage volumes detected; 2 stale service keys rotated."),
                ],
            )
