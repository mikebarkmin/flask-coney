import json
from uuid import uuid4

from flask_coney.encoder import UUIDEncoder


def test_encode_with_uuid():
    id = uuid4()
    pure = {"id": id, "name": "Hi", "list": []}

    encoded = json.dumps(pure, cls=UUIDEncoder)

    assert str(id) in encoded


def test_encode_without_uuid():
    pure = {"name": "Hi", "list": []}

    encoded = json.dumps(pure, cls=UUIDEncoder)

    assert json.dumps(pure) == encoded
