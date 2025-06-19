import os, requests


API = os.getenv("API_ADDR", "localhost")
PORT = os.getenv("API_PORT", "8000")
LOG = os.getenv("LOG", "0") == "1"

tests = [
    ("life is beautiful", True),
    ("that sucks", False),
]
versions = ["/v1/sentiment", "/v2/sentiment"]

out = "\n──── Content ────\n"
for endpoint in versions:
    for text, expect_pos in tests:
        resp  = requests.get(
            f"http://{API}:{PORT}{endpoint}",
            params={"username": "alice", "password": "wonderland", "sentence": text}
        )
        score = resp.json().get("score", 0.0)
        is_pos = score > 0
        result = "SUCCESS" if is_pos == expect_pos else "FAILURE"
        exp_str= "positive" if expect_pos else "negative"
        out += f"{endpoint} '{text}' -> expect {exp_str}, got {score:.4f} -> {result}\n"

print(out)
if LOG:
    with open("/api_output/api_test.log", "a") as f:
        f.write(out)
