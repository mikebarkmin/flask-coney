import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    """Custom JSONEncoder to support UUID objects"""

    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
