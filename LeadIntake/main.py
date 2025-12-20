import json
from datetime import datetime, timezone
import azure.functions as func

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400"
}

def main(req: func.HttpRequest, outBlob: func.Out[str]) -> func.HttpResponse:
    # CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse("", status_code=204, headers=CORS_HEADERS)

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Invalid JSON."}),
            status_code=400,
            mimetype="application/json",
            headers=CORS_HEADERS
        )

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not phone:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Name and phone required."}),
            status_code=400,
            mimetype="application/json",
            headers=CORS_HEADERS
        )

    lead = {
        "received_utc": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "message": message,
        "source": "github-pages-form"
    }

    # Write to blob via output binding (no SDK needed)
    outBlob.set(json.dumps(lead, indent=2))

    return func.HttpResponse(
        json.dumps({"ok": True, "stored": True}),
        status_code=200,
        mimetype="application/json",
        headers=CORS_HEADERS
    )
