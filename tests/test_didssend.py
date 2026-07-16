from voipms.entities.didssend import valid_url


def test_top_level_package_imports_with_current_validators():
    import voipms

    assert voipms.__version__


def test_valid_url_accepts_true_result():
    assert valid_url("https://voip.ms/themes/voipms/assets/img/talent.jpg?v=2")


def test_valid_url_rejects_invalid_result():
    assert not valid_url("not a url")
