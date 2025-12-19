import json
import logging
import azure.functions as func

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Handle CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            "",
            status_code=204,
            headers=CORS_HEADERS
        )

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Invalid JSON"}),
            status_code=400,
            headers=CORS_HEADERS,
            mimetype="application/json"
        )

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not name or not phone:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Name and phone required"}),
            status_code=400,
            headers=CORS_HEADERS,
            mimetype="application/json"
        )

    logging.info(f"Lead received: {name} {phone}")

    return func.HttpResponse(
        json.dumps({"ok": True}),
        status_code=200,
        headers=CORS_HEADERS,
        mimetype="application/json"
    )
