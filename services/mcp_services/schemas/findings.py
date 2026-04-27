from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class NumericalSeverity(str, Enum):
    S0 = "S0"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"

class Finding(BaseModel):
    title: str
    test: int
    active: bool
    verified: bool
    severity: Severity
    description: str
    found_by:List[int]
    numerical_severity: NumericalSeverity
    mitigated: Optional[str] = None
    mitigated_by: Optional[int] = None
    thread_id: Optional[int] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None
    push_to_jira: Optional[bool] = None
    vulnerability_ids: Optional[List[dict]] = None
    reporter: Optional[int] = None
    date: Optional[str] = None
    sla_start_date: Optional[str] = None
    sla_expiration_date: Optional[str] = None
    cwe: Optional[int] = None
    epss_score: Optional[float] = None
    epss_percentile: Optional[float] = None
    known_exploited: Optional[bool] = None
    ransomware_used: Optional[bool] = None
    kev_date: Optional[str] = None
    cvssv3: Optional[str] = None
    cvssv3_score: Optional[float] = None
    cvssv4: Optional[str] = None
    cvssv4_score: Optional[float] = None
    mitigation: Optional[str] = None
    fix_available: Optional[bool] = None
    fix_version: Optional[str] = None
    impact: Optional[str] = None
    steps_to_reproduce: Optional[str] = None
    severity_justification: Optional[str] = None
    references: Optional[str] = None
    false_p: Optional[bool] = None
    duplicate: Optional[bool] = None
    out_of_scope: Optional[bool] = None
    risk_accepted: Optional[bool] = None
    under_review: Optional[bool] = None
    under_defect_review: Optional[bool] = None
    is_mitigated: Optional[bool] = None
    line: Optional[int] = None
    file_path: Optional[str] = None
    component_name: Optional[str] = None
    component_version: Optional[str] = None
    static_finding: Optional[bool] = None
    dynamic_finding: Optional[bool] = None
    unique_id_from_tool: Optional[str] = None
    vuln_id_from_tool: Optional[str] = None
    sast_source_object: Optional[str] = None
    sast_sink_object: Optional[str] = None
    sast_source_line: Optional[int] = None
    sast_source_file_path: Optional[str] = None
    nb_occurences: Optional[int] = None
    publish_date: Optional[str] = None
    service: Optional[str] = None
    planned_remediation_date: Optional[str] = None
    planned_remediation_version: Optional[str] = None
    effort_for_fixing: Optional[str] = None
    review_requested_by: Optional[int] = None
    defect_review_requested_by: Optional[int] = None
    sonarqube_issue: Optional[int] = None
    reviewers: Optional[List[int]] = None

class FindingUpdate(Finding):
    title: Optional[str] = None
    test: Optional[int] = None
    active: Optional[bool] = None
    verified: Optional[bool] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    found_by: Optional[List[int]] = None
    numerical_severity: Optional[str] = None
