from flask import jsonify

def success_response(data=None, status = 200, meta = None):
    body = {
        "success": True,
        "data": data,
        "error": None
    }
    if meta is not None:
        body["meta"] = meta

    return jsonify(body), status
def error_response(message, status=400):

    return jsonify ({
        "success": False,
        "data": None,
        "error" : message
    }), status