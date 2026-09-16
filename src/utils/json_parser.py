import json

def extract_error_message(resp):
    try:
        data = resp.json()
        if isinstance(data, dict) and "error" in data:
            err = data["error"]
            if isinstance(err, dict):
                return err.get("message", str(err))
            return str(err)
        return json.dumps(data)[:300]
    except (ValueError, json.JSONDecodeError):
        return resp.text[:200] if resp.text else f"Error {resp.status_code}"
