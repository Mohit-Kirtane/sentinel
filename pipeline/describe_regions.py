import base64
import io

from PIL import Image

DESCRIBE_PROMPT = "Describe the masked region in detail, including what it is doing."

# The DAM server (NVlabs/describe-anything's dam_server.py) exposes an
# OpenAI-compatible chat completions API. A region is specified by encoding
# a binary mask into the alpha channel of the input image, per
# https://github.com/NVlabs/describe-anything/blob/main/examples/query_dam_server.py
#
# This module only builds the request/parses the response - running the
# actual server requires a GPU (nvidia/DAM-3B-Video) and is done manually in
# the offline notebook, never in the deployed app.


def build_masked_image_payload(frame_path: str, box: list[float]) -> str:
    """Build a base64 data URL of `frame_path` with alpha set to 255 inside `box`, 0 outside."""
    image = Image.open(frame_path).convert("RGB")
    mask = Image.new("L", image.size, 0)
    x1, y1, x2, y2 = [int(round(v)) for v in box]
    mask.paste(255, (x1, y1, x2, y2))

    rgba = Image.merge("RGBA", image.split() + (mask,))
    buffer = io.BytesIO()
    rgba.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def describe_region(
    frame_path: str,
    box: list[float],
    client,
    model: str = "describe_anything_model",
) -> str:
    """Ask a DAM server (via an OpenAI-compatible client) to describe the masked region."""
    image_payload = build_masked_image_payload(frame_path, box)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_payload}},
                    {"type": "text", "text": DESCRIBE_PROMPT},
                ],
            }
        ],
        max_tokens=512,
        temperature=0.2,
        top_p=0.5,
    )
    return response.choices[0].message.content
