import os, requests


API = os.getenv("API_ADDR", "localhost")
PORT= os.getenv("API_PORT", "8000")
LOG = os.getenv("LOG", "0") == "1"

cases = [
    ("bob", "builder", "/v1/sentiment", "good", 200),
    ("bob", "builder", "/v2/sentiment", "good", 403),

    ("alice", "wonderland", "/v1/sentiment", "great", 200),
    ("alice", "wonderland", "/v2/sentiment", "great", 200),
]

out = "\n──── Authorisation ────\n"
for user, pw, endpoint, sent, expect in cases:
    r = requests.get(
        f"http://{API}:{PORT}{endpoint}",
        params = {"username": user, "password": pw, "sentence": sent}
    )
    status = "SUCCESS" if r.status_code == expect else "FAILURE"
    out += f"{user}@{endpoint} -> exp {expect}, got {r.status_code} -> {status}\n"

print(out)
if LOG:
    with open("/api_output/api_test.log", "a") as f:
        f.write(out)
