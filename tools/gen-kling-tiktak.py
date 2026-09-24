import json
import os
import sys
import time
from pathlib import Path

import requests


API = "https://api.kie.ai/api/v1"
MODEL = "kling/v2-5-turbo-image-to-video-pro"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"


def upload_image(path, key):
    source = Path(path)
    with source.open("rb") as handle:
        response = requests.post(
            UPLOAD_URL,
            headers={"Authorization": f"Bearer {key}"},
            files={"file": (source.name, handle)},
            data={"uploadPath": "kling-tiktak", "fileName": source.name},
            timeout=60,
        )
    response.raise_for_status()
    data = response.json().get("data") or {}
    return data.get("downloadUrl") or data["fileUrl"]


def main():
    key_path = Path.home() / ".claude" / "kie_api_key.txt"
    key = os.environ.get("KIE_API_KEY") or key_path.read_text(encoding="utf-8").strip()
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    prompt = """Mechanically accurate rigid-body Tik-Tak pantograph unfolding. Use the supplied folded Bali 5 DK as the exact first frame and the supplied unfolded Bali 5 DK as the exact final frame.

There are no loose cushions. Never create or remove cushions. The backrest is exactly two rigid upholstered hinged sections. Stationary parts: both armrests and main structural base. Moving front assembly: the complete seat, rigid platform and upholstered front fascia, permanently connected and moving as one solid rectangular part.

Movement must be strictly sequential:
1. Start fully folded: seat horizontal inside frame, two backrest sections upright.
2. Lift the entire seat assembly slightly while metal pantograph arms rotate upward and forward around fixed pivots. Seat and front fascia stay horizontal and connected.
3. Pantograph arms carry the whole seat forward and slightly upward in one arc. The rear edge passes above the rigid front rail. It never enters or intersects the frame, ribs or armrests.
4. Lower the whole seat onto its forward support legs. It stops completely in front of the base. No wheels, rollers, drawer, rails or telescoping section. Backrest stays upright until this stop.
5. Only now rotate both rigid backrest sections forward together around their lower hinges into the empty rear space. Keep their exact thickness, shape and stitching. They never cross or enter the seat.
6. Backrest settles horizontally behind the forward seat. These remain two separate rigid surfaces with a visible straight joint, forming a 202 by 160 cm bed.

Preserve exact Bali 5 DK construction: 236 cm width, wide proportions, terracotta fabric and color, stitching grid, exactly two backrest sections, seat divisions, thick upholstered arm fronts, dark wooden open shelves in both arms, MDF base, rigid frame and feet. No lamellas. No component may bend, morph, melt, stretch, shrink, overlap, merge or pass through another. The sofa cannot fold into itself.

Fixed camera, fixed white studio background. No zoom, cuts, people, hands, text, arrows or dimensions. Prioritize collision-free mechanical movement."""
    start_url = upload_image("assets/bali-5-dk-standart/kling-tiktak-clean-v1/20260907_171422_8f00c30b3148ef68fbb88661fc23485e_1.jpeg", key)
    end_url = upload_image("assets/bali-5-dk-standart/kling-tiktak-clean-v1/20260907_171559_7853bcdccfb63269edfa87ee6dc8c712_1.jpeg", key)
    payload = {
        "model": MODEL,
        "input": {
            "prompt": prompt,
            "image_url": start_url,
            "tail_image_url": end_url,
            "duration": "5",
        },
    }
    response = requests.post(f"{API}/jobs/createTask", headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    body = response.json()
    if body.get("code") not in (None, 200):
        raise RuntimeError(body)
    task_id = body["data"]["taskId"]
    print(f"TASK_ID={task_id}", flush=True)
    for _ in range(120):
        time.sleep(5)
        status = requests.get(
            f"{API}/jobs/recordInfo", headers=headers, params={"taskId": task_id}, timeout=60
        )
        status.raise_for_status()
        data = status.json().get("data") or {}
        state = data.get("state")
        print(f"STATE={state}", flush=True)
        if state == "success":
            result = json.loads(data["resultJson"])
            url = result["resultUrls"][0]
            output = Path("assets/bali-5-dk-standart/video_tiktak-bali-v5.mp4")
            video = requests.get(url, timeout=180)
            video.raise_for_status()
            output.write_bytes(video.content)
            print(f"OUTPUT={output.resolve()}", flush=True)
            return
        if state in {"fail", "failed"}:
            raise RuntimeError(data.get("failMsg") or data)
    raise TimeoutError(f"Kling task did not finish: {task_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR={exc}", file=sys.stderr, flush=True)
        raise
