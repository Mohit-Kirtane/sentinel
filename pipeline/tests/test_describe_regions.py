import base64
import io

from PIL import Image

from pipeline.describe_regions import build_masked_image_payload, describe_region


def _decode(data_url: str) -> Image.Image:
    _, b64 = data_url.split(",", 1)
    return Image.open(io.BytesIO(base64.b64decode(b64)))


def test_masked_image_has_alpha_set_only_inside_the_box(tmp_path):
    frame_path = tmp_path / "frame.png"
    Image.new("RGB", (100, 100), color=(10, 20, 30)).save(frame_path)

    data_url = build_masked_image_payload(str(frame_path), box=[10, 10, 40, 40])
    decoded = _decode(data_url)

    assert decoded.mode == "RGBA"
    alpha = decoded.getchannel("A")
    assert alpha.getpixel((25, 25)) == 255  # inside the box
    assert alpha.getpixel((0, 0)) == 0  # outside the box


def test_describe_region_sends_the_masked_image_and_returns_the_description(tmp_path):
    frame_path = tmp_path / "frame.png"
    Image.new("RGB", (50, 50), color=(1, 2, 3)).save(frame_path)

    class _FakeMessage:
        content = "A person in a blue jacket stands near the door."

    class _FakeChoice:
        message = _FakeMessage()

    class _FakeResponse:
        choices = [_FakeChoice()]

    class _FakeCompletions:
        def create(self, **kwargs):
            assert kwargs["model"] == "describe_anything_model"
            content = kwargs["messages"][0]["content"]
            assert content[0]["type"] == "image_url"
            assert content[0]["image_url"]["url"].startswith("data:image/png;base64,")
            return _FakeResponse()

    class _FakeChat:
        completions = _FakeCompletions()

    class _FakeClient:
        chat = _FakeChat()

    description = describe_region(str(frame_path), box=[5, 5, 20, 20], client=_FakeClient())

    assert description == "A person in a blue jacket stands near the door."
