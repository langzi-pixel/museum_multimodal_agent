from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.pipeline import MuseumAgentPipeline
from app.schemas import ArtifactInput


def main():
    pipeline = MuseumAgentPipeline()
    item = ArtifactInput(
        aid="demo_fuhao_xiaozun_001",
        collection_name="妇好鸮尊",
        original_description="“妇好”鸮尊是商代晚期青铜酒器，1976年出土于河南安阳殷墟妇好墓。器物作鸮鸟形，造型稳重，纹饰精美。",
        image_path="sample_data/images/fuhao_xiaozun_demo.jpg",
        position="河南博物院主展馆",
        category_name="镇院之宝",
    )
    result = pipeline.process_one(item)
    out = ROOT / "runtime" / "demo_result.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    print(f"[OK] Demo finished: {out}")
    print(f"[OK] Generated styles: {len(result.styles)}")
    print(f"[OK] First audio: {result.styles[0].audio_url}")


if __name__ == "__main__":
    main()
