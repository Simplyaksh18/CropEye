# sample function code: app.py
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = {"soil_moisture": 0.35, "timestamp": "2025-09-28T06:00:00Z"}
    return func.HttpResponse(json.dumps(data), mimetype="application/json")
