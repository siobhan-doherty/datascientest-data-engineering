import os, requests


API = os.getenv("API_ADDR", "localhost")
PORT= os.getenv("API_PORT", "8000")
LOG = os.getenv("LOG", "0") == "1"

cases = [
    ("alice", "wonderland", 200),
    ("bob", "builder", 200),
    ("clementine", "mandarine", 403),
]

out = "\n──── Authentication ────\n"
for user, pw, expect in cases:
    r = requests.get(
        f"http://{API}:{PORT}/permissions",
        params = {"username": user, "password": pw}
    )
    status = "SUCCESS" if r.status_code == expect else "FAILURE"
    out += f"{user}:{pw} -> expected {expect}, got {r.status_code} -> {status}\n"

print(out)
if LOG:
    with open("/api_output/api_test.log", "a") as f:
        f.write(out)
