import json
import azure.functions as func

ALLOWED_ORIGIN = "https://cornerstoneleadgroup.github.io"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
    "Vary": "Origin",
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

def main(req: func.HttpRequest, outBlob: func.Out[str]) -> func.HttpResponse:
    # CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse("", status_code=204, headers=CORS_HEADERS)

    try:
        data = req.get_json()
    except ValueError:
        return _resp(400, {"ok": False, "error": "Invalid JSON"})

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not phone:
        return _resp(400, {"ok": False, "error": "Name and phone required."})

    lead = {
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "message": message,
        "source": "github-pages-form"
    }

    outBlob.set(json.dumps(lead, indent=2))
    return _resp(200, {"ok": True, "stored": True})
