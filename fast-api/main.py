from fastapi import FastAPI # type: ignore


api = FastAPI()
data = [1, 2, 3, 4, 5]

@api.get("/data")
def get_data(index):
    return {
        "data": data[int(index)]
    }
