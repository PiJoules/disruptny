from sms import *
from flask import Flask, request, jsonify

app = Flask(__name__)


class JSONResp:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def jsonify(self):
        return jsonify(
            code=self.code,
            msg=self.msg
        )


class Success(JSONResp):
    def __init__(self):
        super().__init__(
            0,
            "Message sent successfully"
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
    args = request.get_json(force=True)

    if not args.get("targets", None):
        return EmptyTargets().jsonify()

    msg = args.get("msg", "").strip()
    if not msg:
        return EmptyMessage().jsonify()

    try:
        send_many(args["targets"], msg)
    except NeximoException as e:
        return NeximoError(e.code, e.msg).jsonify()

    return Success().jsonify()


def test_send


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )
