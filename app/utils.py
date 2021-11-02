from flask import jsonify
import json
from app import db
from app.errors import NotFoundError


def get_all_json(tablename: str) -> json:
    if not (res := db.engine.execute(f'select * from {tablename}')):
        raise NotFoundError
    return jsonify([dict(r) for r in res])


def get_json(tablename: str, uid: int) -> json:
    if not (res := db.engine.execute(f'select * from {tablename} where id = {uid}').first()):
        raise NotFoundError
    return jsonify(dict(res))
