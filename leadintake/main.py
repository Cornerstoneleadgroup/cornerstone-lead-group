import json
import azure.functions as func

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400"
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse("", status_code=204, headers=CORS_HEADERS)

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json",
            headers=CORS_HEADERS
        )

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not name or not phone:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Name and phone required."}),
            status_code=400,
            mimetype="application/json",
            headers=CORS_HEADERS
        )

    return func.HttpResponse(
        json.dumps({"ok": True, "msg": f"Hello, {name}. LeadIntake is alive."}),
        status_code=200,
        mimetype="application/json",
        headers=CORS_HEADERS
    )
