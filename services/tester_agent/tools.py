import os
import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# ---------------------------------------------------------------------------
# MCP endpoint configuration
# ---------------------------------------------------------------------------
MCP_SERVICE_BASE_URL = os.getenv("MCP_SERVICE_BASE_URL", "http://localhost:8081")
MCP_ENDPOINT = f"{MCP_SERVICE_BASE_URL}/mcp"


# ---------------------------------------------------------------------------
# Generic MCP caller — every tool goes through this
# ---------------------------------------------------------------------------
async def call_mcp_tool(tool_name: str, arguments: dict) -> Any:
    """
    Opens a fresh streamable-HTTP MCP session, calls the named tool,
    and returns the content payload.
    """
    async with streamablehttp_client(MCP_ENDPOINT) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            # result.content is a list of ContentBlock objects.
            # If there is exactly one text block, unwrap it to a plain dict/str
            # so the ReAct loop can handle it easily.
            if result.content and len(result.content) == 1:
                block = result.content[0]
                if hasattr(block, "text"):
                    try:
                        return json.loads(block.text)
                    except (json.JSONDecodeError, TypeError):
                        return block.text
            return result.content


# ===========================================================================
# Pydantic input models
# ===========================================================================

# --- Engagements ---
class ListEngagementsInput(BaseModel):
    limit: Optional[int] = Field(20, description="Max engagements to return.")
    offset: Optional[int] = Field(0, description="Items to skip.")

class GetEngagementInput(BaseModel):
    engagement_id: int = Field(..., description="ID of the engagement.")

class UpdateEngagementInput(BaseModel):
    engagement_id: int = Field(..., description="ID of the engagement to update.")
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    product: Optional[int] = None
    lead: Optional[int] = None
    tags: Optional[List[str]] = None
    active: Optional[bool] = None
    test_start: Optional[str] = None
    test_end: Optional[str] = None

class RunEngagementPipelineInput(BaseModel):
    product_id: int = Field(..., description="Product this engagement belongs to.")
    name: str = Field(..., description="Engagement name.")
    description: Optional[str] = None
    status: Optional[str] = Field("In Progress")
    lead: Optional[int] = None
    target_start: Optional[str] = None
    target_end: Optional[str] = None

# --- Findings ---
class ListFindingsInput(BaseModel):
    limit: Optional[int] = Field(20)
    offset: Optional[int] = Field(0)
    test: Optional[int] = Field(None, description="Filter by test ID.")
    product: Optional[int] = Field(None, description="Filter by product ID.")

class GetFindingInput(BaseModel):
    finding_id: int = Field(..., description="ID of the finding.")

class UpdateFindingInput(BaseModel):
    finding_id: int = Field(..., description="ID of the finding to update.")
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    active: Optional[bool] = None
    mitigated: Optional[bool] = None
    mitigated_by: Optional[int] = None
    cve: Optional[str] = None
    references: Optional[str] = None
    numerical_severity: Optional[str] = None

class RunFindingPipelineInput(BaseModel):
    test_id: int = Field(..., description="Test this finding is associated with.")
    title: str = Field(..., description="Finding title.")
    severity: str = Field(..., description="e.g. Critical / High / Medium / Low / Informational.")
    description: Optional[str] = None
    active: Optional[bool] = True
    verified: Optional[bool] = False
    cve: Optional[str] = None
    references: Optional[str] = None
    date: Optional[str] = None

# --- Products ---
class ListProductsInput(BaseModel):
    limit: Optional[int] = Field(50)
    offset: Optional[int] = Field(0)
    name: Optional[str] = None

class GetProductInput(BaseModel):
    product_id: int = Field(..., description="ID of the product.")

class UpdateProductInput(BaseModel):
    product_id: int = Field(..., description="ID of the product to update.")
    name: Optional[str] = None
    description: Optional[str] = None
    prod_type: Optional[int] = None
    authorized_users: Optional[List[int]] = None
    product_manager: Optional[int] = None

class RunProductPipelineInput(BaseModel):
    product_type_id: int = Field(..., description="Product type this product belongs to.")
    name: str = Field(..., description="Product name.")
    description: Optional[str] = None

# --- Product Types ---
class ListProductTypesInput(BaseModel):
    limit: Optional[int] = Field(50)
    offset: Optional[int] = Field(0)
    name: Optional[str] = None

class GetProductTypeInput(BaseModel):
    product_type_id: int = Field(..., description="ID of the product type.")

class UpdateProductTypeInput(BaseModel):
    product_type_id: int = Field(..., description="ID of the product type to update.")
    name: Optional[str] = None

class RunProductTypePipelineInput(BaseModel):
    product_type_name: str = Field(..., description="Name of the product type to ensure exists.")

# --- Tests ---
class ListTestsInput(BaseModel):
    limit: Optional[int] = Field(50)
    offset: Optional[int] = Field(0)
    engagement: Optional[int] = Field(None, description="Filter by engagement ID.")

class GetTestInput(BaseModel):
    test_id: int = Field(..., description="ID of the test.")

class UpdateTestInput(BaseModel):
    test_id: int = Field(..., description="ID of the test to update.")
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    test_type: Optional[int] = None
    percent_complete: Optional[int] = None
    environment: Optional[int] = None

class RunTestPipelineInput(BaseModel):
    engagement_id: int = Field(..., description="Engagement this test belongs to.")
    title: str = Field(..., description="Test title.")
    test_type: int = Field(..., description="ID of the test type.")
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = Field("In Progress")

# --- Test Types ---
class ListTestTypesInput(BaseModel):
    limit: Optional[int] = Field(50)
    offset: Optional[int] = Field(0)
    name: Optional[str] = None

class GetTestTypeInput(BaseModel):
    test_type_id: int = Field(..., description="ID of the test type.")

class CreateTestTypeInput(BaseModel):
    name: str = Field(..., description="Name of the new test type.")

class RunTestTypePipelineInput(BaseModel):
    name: str = Field(..., description="Test type name to ensure exists.")


# ===========================================================================
# Tool functions — thin wrappers over call_mcp_tool()
# ===========================================================================

# --- Engagements ---
async def list_engagements_tool(input: ListEngagementsInput) -> Any:
    """Lists engagements with optional pagination."""
    return await call_mcp_tool("list_engagements", input.dict(exclude_none=True))

async def get_engagement_tool(input: GetEngagementInput) -> Any:
    """Gets a single engagement by ID."""
    return await call_mcp_tool("get_engagement", {"engagement_id": input.engagement_id})

async def update_engagement_tool(input: UpdateEngagementInput) -> Any:
    """Updates an existing engagement."""
    args = input.dict(exclude_unset=True)
    return await call_mcp_tool("update_engagement", args)

async def delete_engagement_tool(input: GetEngagementInput) -> Any:
    """Deletes an engagement by ID. Irreversible."""
    return await call_mcp_tool("delete_engagement", {"engagement_id": input.engagement_id})

async def run_engagement_pipeline_tool(input: RunEngagementPipelineInput) -> Any:
    """Creates or reuses an engagement for the given product."""
    return await call_mcp_tool("run_engagement_pipeline", input.dict(exclude_unset=True))

# --- Findings ---
async def list_findings_tool(input: ListFindingsInput) -> Any:
    """Lists findings with optional filters (test, product)."""
    return await call_mcp_tool("list_findings", input.dict(exclude_none=True))

async def get_finding_tool(input: GetFindingInput) -> Any:
    """Gets a single finding by ID."""
    return await call_mcp_tool("get_finding", {"finding_id": input.finding_id})

async def update_finding_tool(input: UpdateFindingInput) -> Any:
    """Updates an existing finding."""
    return await call_mcp_tool("update_finding", input.dict(exclude_unset=True))

async def delete_finding_tool(input: GetFindingInput) -> Any:
    """Deletes a finding by ID. Irreversible."""
    return await call_mcp_tool("delete_finding", {"finding_id": input.finding_id})

async def run_finding_pipeline_tool(input: RunFindingPipelineInput) -> Any:
    """Creates or updates a finding based on title + test ID."""
    return await call_mcp_tool("run_finding_pipeline", input.dict(exclude_unset=True))

# --- Products ---
async def list_products_tool(input: ListProductsInput) -> Any:
    """Lists products with optional name filter."""
    return await call_mcp_tool("list_products", input.dict(exclude_none=True))

async def get_product_tool(input: GetProductInput) -> Any:
    """Gets a single product by ID."""
    return await call_mcp_tool("get_product", {"product_id": input.product_id})

async def update_product_tool(input: UpdateProductInput) -> Any:
    """Updates an existing product."""
    return await call_mcp_tool("update_product", input.dict(exclude_unset=True))

async def delete_product_tool(input: GetProductInput) -> Any:
    """Deletes a product by ID. Irreversible."""
    return await call_mcp_tool("delete_product", {"product_id": input.product_id})

async def run_product_pipeline_tool(input: RunProductPipelineInput) -> Any:
    """Creates or reuses a product by name under the given product type."""
    return await call_mcp_tool("run_product_pipeline", input.dict(exclude_unset=True))

# --- Product Types ---
async def list_product_types_tool(input: ListProductTypesInput) -> Any:
    """Lists product types with optional name filter."""
    return await call_mcp_tool("list_product_types", input.dict(exclude_none=True))

async def get_product_type_tool(input: GetProductTypeInput) -> Any:
    """Gets a single product type by ID."""
    return await call_mcp_tool("get_product_type", {"product_type_id": input.product_type_id})

async def update_product_type_tool(input: UpdateProductTypeInput) -> Any:
    """Updates an existing product type."""
    return await call_mcp_tool("update_product_type", input.dict(exclude_unset=True))

async def delete_product_type_tool(input: GetProductTypeInput) -> Any:
    """Deletes a product type by ID. Irreversible."""
    return await call_mcp_tool("delete_product_type", {"product_type_id": input.product_type_id})

async def run_product_type_pipeline_tool(input: RunProductTypePipelineInput) -> Any:
    """Ensures a product type exists by name, creating it if necessary."""
    return await call_mcp_tool("run_product_type_pipeline", input.dict(exclude_unset=True))

# --- Tests ---
async def list_tests_tool(input: ListTestsInput) -> Any:
    """Lists tests with optional engagement filter."""
    return await call_mcp_tool("list_tests", input.dict(exclude_none=True))

async def get_test_tool(input: GetTestInput) -> Any:
    """Gets a single test by ID."""
    return await call_mcp_tool("get_test", {"test_id": input.test_id})

async def update_test_tool(input: UpdateTestInput) -> Any:
    """Updates an existing test."""
    return await call_mcp_tool("update_test", input.dict(exclude_unset=True))

async def delete_test_tool(input: GetTestInput) -> Any:
    """Deletes a test by ID. Irreversible."""
    return await call_mcp_tool("delete_test", {"test_id": input.test_id})

async def run_test_pipeline_tool(input: RunTestPipelineInput) -> Any:
    """Creates or reuses a test by title + engagement ID."""
    return await call_mcp_tool("run_test_pipeline", input.dict(exclude_unset=True))

# --- Test Types ---
async def list_test_types_tool(input: ListTestTypesInput) -> Any:
    """Lists test types with optional name filter."""
    return await call_mcp_tool("list_test_types", input.dict(exclude_none=True))

async def get_test_type_tool(input: GetTestTypeInput) -> Any:
    """Gets a single test type by ID."""
    return await call_mcp_tool("get_test_type", {"test_type_id": input.test_type_id})

async def create_test_type_tool(input: CreateTestTypeInput) -> Any:
    """Creates a brand new test type."""
    return await call_mcp_tool("create_test_type", input.dict(exclude_unset=True))

async def run_test_type_pipeline_tool(input: RunTestTypePipelineInput) -> Any:
    """Ensures a test type exists by name, creating it if necessary."""
    return await call_mcp_tool("run_test_type_pipeline", input.dict(exclude_unset=True))


# ===========================================================================
# AGENT_TOOLS — fed directly into the ReAct loop
# ===========================================================================
AGENT_TOOLS = [
    # --- Engagements ---
    {
        "name": "list_engagements",
        "description": "Retrieve a paginated list of engagements. Filters: limit (int), offset (int).",
        "function": list_engagements_tool,
        "input_schema": json.dumps(ListEngagementsInput.model_json_schema()),
    },
    {
        "name": "get_engagement_by_id",
        "description": "Get full details of a single engagement by its ID.",
        "function": get_engagement_tool,
        "input_schema": json.dumps(GetEngagementInput.model_json_schema()),
    },
    {
        "name": "update_existing_engagement",
        "description": "Modify an existing engagement (status, name, description, etc.). Requires engagement_id plus any fields to change.",
        "function": update_engagement_tool,
        "input_schema": json.dumps(UpdateEngagementInput.model_json_schema()),
    },
    {
        "name": "delete_engagement_by_id",
        "description": "Permanently delete an engagement by ID. Irreversible.",
        "function": delete_engagement_tool,
        "input_schema": json.dumps(GetEngagementInput.model_json_schema()),
    },
    {
        "name": "manage_engagement_pipeline",
        "description": "Create a new engagement or reuse an existing one for a given product. Requires product_id and name.",
        "function": run_engagement_pipeline_tool,
        "input_schema": json.dumps(RunEngagementPipelineInput.model_json_schema()),
    },
    # --- Findings ---
    {
        "name": "list_findings",
        "description": "Retrieve a paginated list of findings. Optional filters: test (int), product (int), limit, offset.",
        "function": list_findings_tool,
        "input_schema": json.dumps(ListFindingsInput.model_json_schema()),
    },
    {
        "name": "get_finding_by_id",
        "description": "Get full details of a single finding by its ID.",
        "function": get_finding_tool,
        "input_schema": json.dumps(GetFindingInput.model_json_schema()),
    },
    {
        "name": "update_existing_finding",
        "description": "Modify an existing finding (severity, title, active, etc.). Requires finding_id plus any fields to change.",
        "function": update_finding_tool,
        "input_schema": json.dumps(UpdateFindingInput.model_json_schema()),
    },
    {
        "name": "delete_finding_by_id",
        "description": "Permanently delete a finding by ID. Irreversible.",
        "function": delete_finding_tool,
        "input_schema": json.dumps(GetFindingInput.model_json_schema()),
    },
    {
        "name": "manage_finding_pipeline",
        "description": "Create or update a finding by title + test ID. Requires test_id, title, and severity.",
        "function": run_finding_pipeline_tool,
        "input_schema": json.dumps(RunFindingPipelineInput.model_json_schema()),
    },
    # --- Products ---
    {
        "name": "list_products",
        "description": "Retrieve a paginated list of products. Optional filter: name (str).",
        "function": list_products_tool,
        "input_schema": json.dumps(ListProductsInput.model_json_schema()),
    },
    {
        "name": "get_product_by_id",
        "description": "Get full details of a single product by its ID.",
        "function": get_product_tool,
        "input_schema": json.dumps(GetProductInput.model_json_schema()),
    },
    {
        "name": "update_existing_product",
        "description": "Modify an existing product (name, description, prod_type, etc.). Requires product_id plus fields to change.",
        "function": update_product_tool,
        "input_schema": json.dumps(UpdateProductInput.model_json_schema()),
    },
    {
        "name": "delete_product_by_id",
        "description": "Permanently delete a product by ID. Irreversible.",
        "function": delete_product_tool,
        "input_schema": json.dumps(GetProductInput.model_json_schema()),
    },
    {
        "name": "manage_product_pipeline",
        "description": "Create or reuse a product by name under a given product type. Requires product_type_id and name.",
        "function": run_product_pipeline_tool,
        "input_schema": json.dumps(RunProductPipelineInput.model_json_schema()),
    },
    # --- Product Types ---
    {
        "name": "list_product_types",
        "description": "Retrieve a paginated list of product types. Optional filter: name (str).",
        "function": list_product_types_tool,
        "input_schema": json.dumps(ListProductTypesInput.model_json_schema()),
    },
    {
        "name": "get_product_type_by_id",
        "description": "Get full details of a single product type by its ID.",
        "function": get_product_type_tool,
        "input_schema": json.dumps(GetProductTypeInput.model_json_schema()),
    },
    {
        "name": "update_existing_product_type",
        "description": "Modify an existing product type name. Requires product_type_id and name.",
        "function": update_product_type_tool,
        "input_schema": json.dumps(UpdateProductTypeInput.model_json_schema()),
    },
    {
        "name": "delete_product_type_by_id",
        "description": "Permanently delete a product type by ID. Irreversible.",
        "function": delete_product_type_tool,
        "input_schema": json.dumps(GetProductTypeInput.model_json_schema()),
    },
    {
        "name": "manage_product_type_pipeline",
        "description": "Ensure a product type exists by name, creating it if absent. Requires product_type_name.",
        "function": run_product_type_pipeline_tool,
        "input_schema": json.dumps(RunProductTypePipelineInput.model_json_schema()),
    },
    # --- Tests ---
    {
        "name": "list_tests",
        "description": "Retrieve a paginated list of tests. Optional filter: engagement (int).",
        "function": list_tests_tool,
        "input_schema": json.dumps(ListTestsInput.model_json_schema()),
    },
    {
        "name": "get_test_by_id",
        "description": "Get full details of a single test by its ID.",
        "function": get_test_tool,
        "input_schema": json.dumps(GetTestInput.model_json_schema()),
    },
    {
        "name": "update_existing_test",
        "description": "Modify an existing test (title, status, test_type, etc.). Requires test_id plus fields to change.",
        "function": update_test_tool,
        "input_schema": json.dumps(UpdateTestInput.model_json_schema()),
    },
    {
        "name": "delete_test_by_id",
        "description": "Permanently delete a test by ID. Irreversible.",
        "function": delete_test_tool,
        "input_schema": json.dumps(GetTestInput.model_json_schema()),
    },
    {
        "name": "manage_test_pipeline",
        "description": "Create or reuse a test by title + engagement ID. Requires engagement_id, title, and test_type (ID).",
        "function": run_test_pipeline_tool,
        "input_schema": json.dumps(RunTestPipelineInput.model_json_schema()),
    },
    # --- Test Types ---
    {
        "name": "list_test_types",
        "description": "Retrieve a paginated list of test types. Optional filter: name (str).",
        "function": list_test_types_tool,
        "input_schema": json.dumps(ListTestTypesInput.model_json_schema()),
    },
    {
        "name": "get_test_type_by_id",
        "description": "Get full details of a single test type by its ID.",
        "function": get_test_type_tool,
        "input_schema": json.dumps(GetTestTypeInput.model_json_schema()),
    },
    {
        "name": "create_new_test_type",
        "description": "Create a brand-new test type. Requires name.",
        "function": create_test_type_tool,
        "input_schema": json.dumps(CreateTestTypeInput.model_json_schema()),
    },
    {
        "name": "manage_test_type_pipeline",
        "description": "Ensure a test type exists by name, creating it if absent. Requires name.",
        "function": run_test_type_pipeline_tool,
        "input_schema": json.dumps(RunTestTypePipelineInput.model_json_schema()),
    },
]