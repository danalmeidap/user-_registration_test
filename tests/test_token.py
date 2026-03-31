from jwt import decode

from fast_api_zero.token import ALGORITHM, SECRET_KEY, create_access_token


def test_create_access_token():
    data = {'sub': 'testuser'}
    token = create_access_token(data)

    assert isinstance(token, str)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded['sub'] == 'testuser'
    assert 'exp' in decoded
