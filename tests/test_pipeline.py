from app.pipeline import MuseumAgentPipeline
from app.schemas import ArtifactInput


def test_process_one_mock():
    p = MuseumAgentPipeline()
    item = ArtifactInput(
        aid="test001",
        collection_name="妇好鸮尊",
        original_description="商代晚期青铜器。",
    )
    result = p.process_one(item)
    assert result.knowledge.artifact_name
    assert len(result.styles) == 8
    assert result.sync_status == "success"
