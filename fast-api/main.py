from fastapi import FastAPI, Header


api = FastAPI()

@api.get('/headers')
def get_headers(user_agent: str = Header(None)):
    return {
        'User-Agent': user_agent
    }
