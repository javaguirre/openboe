from unicodedata import normalize
from flask import make_response
from bson import json_util
import json


def slug(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):

    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()

    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)

    return ''.join(strict_text)


def make_json_response(body):
    resp = make_response(json.dumps(body, default=json_util.default))
    resp.mimetype = 'application/json'

    return resp
