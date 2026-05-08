from __future__ import annotations
from app.schemas import ArtifactResult
from app.integrations.business_api import BusinessAPI


class SyncAgent:
    """结果回写 Agent。"""

    def __init__(self):
        self.api = BusinessAPI()

    def run(self, result: ArtifactResult) -> ArtifactResult:
        payload = result.model_dump()
        payload["audit_status"] = 3
        payload["type"] = "museum_multimodal_agent_result"
        resp = self.api.sync_artifact_result(payload)
        result.sync_status = "success" if resp.get("code") == 1 else "failed"
        result.sync_response = resp
        return result
