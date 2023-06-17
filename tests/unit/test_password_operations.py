import auth.password as ap

password = "this_is_a_test_password"

def test_hash_password():
    hashed_password = ap.hash_password(password)
    assert ap.verify_password(password, hashed_password)