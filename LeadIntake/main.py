import json
import logging
import azure.functions as func

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400"
}

def _resp(status: int, body: dict):
    return func.HttpResponse(
        json.dumps(body),
        status_code=status,
        mimetype="application/json",
        headers=CORS_HEADERS
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Preflight request
    if req.method == "OPTIONS":
        return func.HttpResponse("", status_code=204, headers=CORS_HEADERS)

    try:
        data = req.get_json()
    except ValueError:
        return _resp(400, {"ok": False, "error": "Invalid JSON. Send a JSON body."})

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not phone:
        return _resp(400, {"ok": False, "error": "Missing required fields: name and phone."})

    lead = {
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "message": message
    }

    logging.info("NEW LEAD RECEIVED: %s", json.dumps(lead))

    return _resp(200, {"ok": True, "received": lead})
