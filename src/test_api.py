from typing import List
from utils.json_parser import extract_error_message
import requests


def test_api_keys(base_url, api_key, timeout=10):
    url = base_url.rstrip('/') + "/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        resp = requests.get(url=url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            return {"ok": True, "status_code": resp.status_code, "message": "OK"}
        return {"ok": False, "status_code": resp.status_code, "message": extract_error_message(resp)}

    except requests.exceptions.Timeout:
        return {"ok": False, "status_code": None, "message": "Timeout Error - Server has a problem"}

    except requests.exceptions.ConnectionError:
        return {"ok": False, "status_code": None, "message": "Connection Error - Check your connection or url"}

    except requests.exceptions.RequestException as e:
        return {"ok": False, "status_code": None, "message": e}

    except Exception as e:
        return {"ok": False, "status_code": None, "message": e}


def test_multiple_keys(base_url, api_keys: List[str], timeout=10):
    results = []

    for api_key in api_keys:
        api_key = api_key.strip()
        if not api_key:
            continue
        res = test_api_keys(base_url, api_key, timeout)
        res["api_key"] = api_key
        results.append(res)
    return results
