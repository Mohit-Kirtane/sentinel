from app.auth.security import create_access_token, decode_access_token, hash_password, verify_password


def test_verify_password_matches_the_correct_password():
    hashed = hash_password("correct-password")
    assert verify_password("correct-password", hashed) is True


def test_verify_password_rejects_a_wrong_password():
    hashed = hash_password("correct-password")
    assert verify_password("wrong-password", hashed) is False


def test_decode_access_token_returns_the_subject_it_was_created_with():
    token = create_access_token("demo")
    assert decode_access_token(token) == "demo"


def test_decode_access_token_returns_none_for_garbage():
    assert decode_access_token("not-a-real-token") is None
