import json
import logging
import os
import uuid
from datetime import datetime, timezone

import azure.functions as func

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400"
}

CONTAINER_NAME = "leads"

def _resp(status: int, body: dict):
    return func.HttpResponse(
        json.dumps(body),
        status_code=status,
        mimetype="application/json",
        headers=CORS_HEADERS
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    # CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse("", status_code=204, headers=CORS_HEADERS)

    # Parse JSON
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
        return _resp(400, {"ok": False, "error": "Name and phone required."})

    lead = {
        "id": str(uuid.uuid4()),
        "received_utc": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "message": message,
        "source": "github-pages-form"
    }

    # --- FORCE THE REAL ERROR TO SHOW UP ---
    try:
        # Lazy import so we can return a JSON error even if the package is missing
        try:
            from azure.storage.blob import BlobServiceClient
        except Exception as e:
            logging.exception("Blob SDK import failed.")
            return _resp(500, {
                "ok": False,
                "error": "Blob SDK import failed",
                "details": str(e)
            })

        conn_str = os.environ.get("AzureWebJobsStorage")
        if not conn_str:
            return _resp(500, {"ok": False, "error": "AzureWebJobsStorage missing in app settings."})

        blob_service = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service.get_container_client(CONTAINER_NAME)

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        blob_name = f"{ts}__{lead['id']}.json"

        container_client.upload_blob(
            name=blob_name,
            data=json.dumps(lead, indent=2),
            overwrite=False
        )

    except Exception as e:
        logging.exception("Blob write failed.")
        return _resp(500, {
            "ok": False,
            "error": "Blob write failed",
            "details": str(e)
        })

    return _resp(200, {"ok": True, "stored": True, "lead_id": lead["id"]})
