from voipms.voipmsclient import VoipMsClient


class FakeResponse:
    status_code = 200

    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_post_sends_multipart_json_request_and_does_not_mutate_parameters(monkeypatch):
    captured = {}

    def fake_post(url, files, timeout):
        captured["url"] = url
        captured["files"] = files
        captured["timeout"] = timeout
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
    assert captured["timeout"] == (5, 20)


def test_request_timeout_is_configurable_for_get_and_post(monkeypatch):
    captured = {}

    def fake_get(url, timeout):
        captured["get_timeout"] = timeout
        return FakeResponse({"status": "success"})

    def fake_post(url, files, timeout):
        captured["post_timeout"] = timeout
        return FakeResponse({"status": "success"})

    monkeypatch.setattr("voipms.voipmsclient.requests.get", fake_get)
    monkeypatch.setattr("voipms.voipmsclient.requests.post", fake_post)

    client = VoipMsClient("user@example.com", "secret", request_timeout=(2, 7))
    client._get("getIP")
    client._post("getBalance")

    assert captured == {"get_timeout": (2, 7), "post_timeout": (2, 7)}
