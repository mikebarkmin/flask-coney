from uuid import uuid4

import pytest

from flask_coney.encoder import UUIDEncoder


def test_encode_uuid():
    id = uuid4()

    encoded = UUIDEncoder().default(id)

    assert str(id) in encoded


def test_encode_not_jsonable():
    encode = [1, 2, 3, 4]

    with pytest.raises(TypeError):
        UUIDEncoder().default(encode)
