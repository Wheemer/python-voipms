from voipms.voipmsclient import VoipMsClient


class FakeResponse:
    status_code = 200

    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_post_sends_json_content_type_and_does_not_mutate_parameters(monkeypatch):
    captured = {}

    def fake_post(url, files):
        captured["url"] = url
        captured["files"] = files
        return FakeResponse({"status": "success", "balance": "1.23"})

    monkeypatch.setattr("voipms.voipmsclient.requests.post", fake_post)
    params = {"advanced": True}

    result = VoipMsClient("user@example.com", "secret")._post("getBalance", params)

    assert result["balance"] == "1.23"
    assert params == {"advanced": True}
    assert captured["files"]["api_username"] == (None, "user@example.com")
    assert captured["files"]["api_password"] == (None, "secret")
    assert captured["files"]["method"] == (None, "getBalance")
    assert captured["files"]["content_type"] == (None, "json")
    assert captured["files"]["advanced"] == (None, "True")
