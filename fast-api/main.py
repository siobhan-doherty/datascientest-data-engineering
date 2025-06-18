from fastapi import FastAPI # type: ignore


api = FastAPI(
    title = "My API",
    description = "My own API powered by FastAPI.",
    version = "1.0.1"
)

@api.get("/", name = "Hello World")
def get_index():
    """Returns greetings"""
    return {"greetings": "welcome"}
