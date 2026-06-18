import json
import os
import subprocess
import tempfile
from pathlib import Path

from app.workers.celery_app import celery_app

REMOTION_DIR = str(Path(__file__).resolve().parents[4] / "apps" / "remotion")
OUTPUT_DIR = str(Path(__file__).resolve().parents[4] / "data" / "renders")


@celery_app.task(bind=True, max_retries=2, default_retry_delay=120)
def render_marketing_video(
    self,
    scenes: list[dict],
    brand_color: str = "#3b82f6",
    composition_id: str = "MarketingVideo",
    output_name: str | None = None,
) -> dict:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_props = json.dumps({"scenes": scenes, "brandColor": brand_color})
    output_file = output_name or f"marketing_video_{self.request.id}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_file)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        f.write(input_props)
        props_file = f.name

    try:
        result = subprocess.run(
            [
                "npx",
                "remotion",
                "render",
                "src/index.ts",
                composition_id,
                output_path,
                "--props",
                props_file,
                "--log",
                "error",
            ],
            cwd=REMOTION_DIR,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Remotion render failed: {result.stderr}")

        return {
            "status": "completed",
            "output_path": output_path,
            "output_file": output_file,
        }
    except subprocess.TimeoutExpired:
        raise self.retry(exc=TimeoutError("Render timed out"), countdown=120)
    except Exception as e:
        raise self.retry(exc=e, countdown=120)
    finally:
        if os.path.exists(props_file):
            os.unlink(props_file)
