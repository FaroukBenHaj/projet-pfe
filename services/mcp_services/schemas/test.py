class Test(BaseModel):
    engagement: int
    test_type: int 
    target_start: datetime
    target_end: datetime
    notes: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    scan_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    percent_complete: Optional[int] = None
    version: Optional[str] = None
    build_id: Optional[str] = None
    commit_hash: Optional[str] = None
    branch_tag: Optional[str] = None
    lead: Optional[int] = None
    environment: Optional[int] = None
    api_scan_configuration: Optional[int] = None
