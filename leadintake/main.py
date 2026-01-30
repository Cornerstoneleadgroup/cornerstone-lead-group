import json
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import os
import uuid

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("LeadIntake function triggered.")

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json"
        )

    # Required fields
    name = data.get("name")
    phone = data.get("phone")

    if not name or not phone:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Name and phone required"}),
            status_code=400,
            mimetype="application/json"
        )

    # Optional fields
    email = data.get("email")
    zip_code = data.get("zip")
    service = data.get("service")
    message = data.get("message")

    # Metadata
    lead_id = f"CLG-{uuid.uuid4().hex[:6].upper()}-{datetime.utcnow().strftime('%Y%m%d')}"
    timestamp_local = datetime.now().strftime("%A %m-%d-%y %I:%M %p CST")

    lead_data = {
        "lead_id": lead_id,
        "timestamp_local": timestamp_local,
        "name": name,
        "phone": phone,
        "email": email,
        "zip": zip_code,
        "service": service,
        "message": message,
        "source": "github-pages-form"
    }

    try:
        connect_str = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client("leads")

        blob_name = f"{datetime.utcnow().isoformat()}_{lead_id}.json"
        blob_client = container_client.get_blob_client(blob_name)

        blob_client.upload_blob(json.dumps(lead_data), overwrite=True)

        except Exception as e:
        logging.exception("Storage error (full exception):")
        return func.HttpResponse(
            json.dumps({"ok": False, "error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps({"ok": True}),
        status_code=200,
        mimetype="application/json"
    )
