import requests
import json

from sms import *
from flask import Flask, request, jsonify

app = Flask(__name__)

FAKE_NUMBER = "FAKE_NUMBER"


class JSONResp:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __eq__(self, o):
        return (
            self.code == o.code and
            self.msg == o.msg and
            type(self) == type(o)
        )

    def __ne__(self, o):
        return not (self == o)


class Success(JSONResp):
    def __init__(self):
        super().__init__(
            0,
            "Message sent successfully"
        )


class NotJSON(JSONResp):
    def __init__(self):
        super().__init__(
            203,
            "JSON data not provided."
        )


class EmptyTargets(JSONResp):
    def __init__(self):
        super().__init__(
            201,
            "Targets not provided."
        )


class EmptyMessage(JSONResp):
    def __init__(self):
        super().__init__(
            202,
            "Empty message provided"
        )


class NeximoError(JSONResp):
    pass


@app.route("/broadcast_custom")
def handle_braodcast_custom():
    args = request.args.to_dict(flat=False)
    targets = args.get("targets", None)

    if not targets:
        return jsonify(EmptyTargets().__dict__)

    msgs = args.get("msg", [])
    if not msgs:
        return jsonify(EmptyMessage().__dict__)

    msg = msgs[0].strip()
    if not msg:
        return jsonify(EmptyMessage().__dict__)

    if FAKE_NUMBER not in set(targets):
        try:
            send_many(targets, msg)
        except NeximoException as e:
            return jsonify(NeximoError(e.code, e.msg).__dict__)

    return jsonify(Success().__dict__)



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
    )

