import hashlib
import json


def json_to_sha256(json_obj):
    return hashlib.sha256(json.dumps(json_obj, sort_keys=True).encode()).hexdigest()


def string_to_sha256(string_obj):
    return hashlib.sha256(string_obj.encode()).hexdigest()