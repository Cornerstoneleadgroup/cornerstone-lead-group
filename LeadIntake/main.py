import json
import logging
import azure.functions as func

def _resp(status: int, body: dict):
    return func.HttpResponse(
        json.dumps(body),
        status_code=status,
        mimetype="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Handle browser "preflight" request for forms/CORS
    if req.method == "OPTIONS":
        return _resp(200, {"ok": True})

    try:
        data = req.get_json()
    except ValueError:
        return _resp(400, {"ok": False, "error": "Invalid JSON. Send a JSON body."})

    # Pull fields (keep it simple)
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    # Minimal validation
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

    # For now, just confirm receipt. Email comes next step.
    return _resp(200, {"ok": True, "received": lead})
