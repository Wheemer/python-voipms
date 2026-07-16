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

    def fake_post(url, data):
        captured["url"] = url
        captured["data"] = data
        return FakeResponse({"status": "success", "balance": "1.23"})

    monkeypatch.setattr("voipms.voipmsclient.requests.post", fake_post)
    params = {"advanced": True}

    result = VoipMsClient("user@example.com", "secret")._post("getBalance", params)

    assert result["balance"] == "1.23"
    assert params == {"advanced": True}
    assert captured["data"]["api_username"] == "user@example.com"
    assert captured["data"]["api_password"] == "secret"
    assert captured["data"]["method"] == "getBalance"
    assert captured["data"]["content_type"] == "json"
    assert captured["data"]["advanced"] is True
