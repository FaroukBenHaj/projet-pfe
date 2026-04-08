# agent/tools.py
import httpx
from langchain.tools import tool
from config import settings
from typing import Optional


class DefectDojoClient:
    def __init__(self):
        self.base_url = settings.defectdojo_url.rstrip("/")
        self.headers = {
            "Authorization": f"Token {settings.defectdojo_api_key}",
            "Content-Type": "application/json",
        }

    def get_product_types(self, params: dict) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/product_types/",
                headers=self.headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def get_product_type(self, product_type_id: int) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/product_types/{product_type_id}/",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def create_product_type(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/product_types/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def update_product_type(self, product_type_id: int, **data) -> dict:
        try:
            response = httpx.patch(
                f"{self.base_url}/api/v2/product_types/{product_type_id}/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def delete_product_type(self, product_type_id: int) -> dict:
        try:
            response = httpx.delete(
                f"{self.base_url}/api/v2/product_types/{product_type_id}/",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return {"deleted": True, "id": product_type_id}
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def get_product(self, product_name: str) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/products/",
                headers=self.headers,
                params={"name": product_name},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def create_product(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/products/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_engagements(self, param: dict) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/engagements/",
                headers=self.headers,
                params=param,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def create_engagement(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/engagements/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_tests(self, param: dict) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/tests/",
                headers=self.headers,
                params=param,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def create_test(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/tests/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_findings(self, param: dict) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/findings/",
                headers=self.headers,
                params=param,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def create_finding(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/findings/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    def create_test_type(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/test_types/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
    def get_test_type(self, test_type_id: int) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/test_types/{test_type_id}/",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

def get_client() -> DefectDojoClient:
    return DefectDojoClient()


# ✅ All tools are now sync (no async def)
@tool
def list_product_types(limit: int = 50, offset: int = 0) -> dict:
    """List all product types with pagination."""
    filters = {"limit": limit}
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = client.get_product_types(filters)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def create_product_type(
    name: str,
    description: Optional[str] = None,
    critical_product: Optional[bool] = False,
    key_product: Optional[bool] = False,
) -> dict:
    """Create a new product type."""
    client = get_client()
    data = {
        "name": name,
        "description": description,
        "critical_product": critical_product,
        "key_product": key_product,
    }
    result = client.create_product_type(**data)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def get_product_type(product_type_id: int) -> dict:
    """Get a specific product type by ID."""
    client = get_client()
    result = client.get_product_type(product_type_id)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def update_product_type(
    product_type_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    critical_product: Optional[bool] = None,
    key_product: Optional[bool] = None,
) -> dict:
    """Update an existing product type."""
    client = get_client()
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if critical_product is not None:
        data["critical_product"] = critical_product
    if key_product is not None:
        data["key_product"] = key_product
    result = client.update_product_type(product_type_id, **data)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def delete_product_type(product_type_id: int) -> dict:
    """Delete a product type by ID."""
    client = get_client()
    result = client.delete_product_type(product_type_id)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}

@tool
def run_pipeline(
    # Product Type
    product_type_name: str,
    # Product
    product_name: str,
    product_description: Optional[str] = "Created by DefectDojo Agent",
    # Engagement
    engagement_name: str = "Default Engagement",
    engagement_description: Optional[str] = None,
    engagement_target_start: str = None,  # "YYYY-MM-DD"
    engagement_target_end: str = None,    # "YYYY-MM-DD"
    # Test
    test_title: str = "Default Test",
    test_type_id: int = 1,               # Must be a valid test type ID in your DD instance
    test_target_start: str = None,        # "YYYY-MM-DD HH:MM:SS"
    test_target_end: str = None,          # "YYYY-MM-DD HH:MM:SS"
    # Finding
    finding_title: str = "",
    finding_description: str = "",
    finding_severity: str = "Medium",     # Info / Low / Medium / High / Critical
    finding_date: str = None,             # "YYYY-MM-DD"
    # Endpoint (optional)
    endpoint_host: Optional[str] = None,
    endpoint_path: Optional[str] = None,
    endpoint_protocol: Optional[str] = None,
) -> dict:
    """
    Full pipeline: resolves or creates ProductType → Product → Engagement → Test → Finding → (optional) Endpoint.
    Matches existing objects by name. Creates them if they don't exist.
    Returns the created finding and all IDs used along the way.
    """
    from datetime import date, datetime

    client = get_client()
    summary = {}

    # ── 1. PRODUCT TYPE ─────────────────────────────────────────────────────
    pt_result = client.get_product_types({"name": product_type_name})
    if "error" in pt_result:
        return {"status": "error", "step": "get_product_type", "error": pt_result["error"]}

    if pt_result.get("count", 0) > 0:
        product_type_id = pt_result["results"][0]["id"]
        summary["product_type"] = {"action": "reused", "id": product_type_id}
    else:
        created = client.create_product_type(name=product_type_name)
        if "error" in created:
            return {"status": "error", "step": "create_product_type", "error": created["error"]}
        product_type_id = created["id"]
        summary["product_type"] = {"action": "created", "id": product_type_id}

    # ── 2. PRODUCT ───────────────────────────────────────────────────────────
    p_result = client.get_product(product_name)
    if "error" in p_result:
        return {"status": "error", "step": "get_product", "error": p_result["error"]}

    if p_result.get("count", 0) > 0:
        product_id = p_result["results"][0]["id"]
        summary["product"] = {"action": "reused", "id": product_id}
    else:
        created = client.create_product(
            name=product_name,
            description=product_description or "Created by DefectDojo Agent",
            prod_type=product_type_id,
        )
        if "error" in created:
            return {"status": "error", "step": "create_product", "error": created["error"]}
        product_id = created["id"]
        summary["product"] = {"action": "created", "id": product_id}

    # ── 3. ENGAGEMENT ────────────────────────────────────────────────────────
    eng_result = client.get_engagements({"name": engagement_name, "product": product_id})
    if "error" in eng_result:
        return {"status": "error", "step": "get_engagement", "error": eng_result["error"]}

    today = date.today().isoformat()

    if eng_result.get("count", 0) > 0:
        engagement_id = eng_result["results"][0]["id"]
        summary["engagement"] = {"action": "reused", "id": engagement_id}
    else:
        created = client.create_engagement(
            name=engagement_name,
            description=engagement_description or "",
            product=product_id,
            target_start=engagement_target_start or today,
            target_end=engagement_target_end or today,
            status="In Progress",
            engagement_type="Interactive",
        )
        if "error" in created:
            return {"status": "error", "step": "create_engagement", "error": created["error"]}
        engagement_id = created["id"]
        summary["engagement"] = {"action": "created", "id": engagement_id}

    # ── 4. TEST ──────────────────────────────────────────────────────────────
    test_result = client.get_tests({"title": test_title, "engagement": engagement_id})
    if "error" in test_result:
        return {"status": "error", "step": "get_test", "error": test_result["error"]}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if test_result.get("count", 0) > 0:
        test_id = test_result["results"][0]["id"]
        summary["test"] = {"action": "reused", "id": test_id}
    else:
        created = client.create_test(
            title=test_title,
            engagement=engagement_id,
            test_type=test_type_id,
            target_start=test_target_start or now,
            target_end=test_target_end or now,
        )
        if "error" in created:
            return {"status": "error", "step": "create_test", "error": created["error"]}
        test_id = created["id"]
        summary["test"] = {"action": "created", "id": test_id}

    # ── 5. FINDING ───────────────────────────────────────────────────────────
    finding = client.create_finding(
        title=finding_title,
        description=finding_description,
        severity=finding_severity,
        test=test_id,
        date=finding_date or date.today().isoformat(),
        active=True,
        verified=False,
        duplicate=False,
    )
    if "error" in finding:
        return {"status": "error", "step": "create_finding", "error": finding["error"]}

    finding_id = finding["id"]
    summary["finding"] = {"action": "created", "id": finding_id}
    return {
        "status": "success",
        "summary": summary,
        "finding_id": finding_id,
    }

# ✅ list_product_types is now included
tools = [list_product_types, run_pipeline , create_product_type, get_product_type, update_product_type, delete_product_type]