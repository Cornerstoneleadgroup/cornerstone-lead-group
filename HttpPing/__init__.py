import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger function 'HttpPing' processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get("name")

    if name:
        message = f"Hello, {name}. Your Cornerstone function is alive and working."
    else:
        message = "Your Cornerstone function is alive. Add ?name=FastPhil to the URL for a custom greeting."

    return func.HttpResponse(
        message,
        status_code=200
    )
