from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

LICENSE_FILE = "licenses.txt"

def load_licenses():
    licenses = {}
    with open(LICENSE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            key, expiry = line.split("|", 1)
            licenses[key.strip()] = expiry.strip()
    return licenses


@app.get("/check")
def check_license(key: str):
    licenses = load_licenses()
    expiry_str = licenses.get(key)

    if not expiry_str:
        return {"valid": False, "reason": "NOT_FOUND"}

    expiry = datetime.strptime(expiry_str, "%Y-%m-%d")

    if expiry < datetime.utcnow():
        return {"valid": False, "reason": "EXPIRED"}

    return {
        "valid": True,
        "expires": expiry_str
    }
