from fastapi import FastAPI, HTTPException # type: ignore


api = FastAPI()
data = [1, 2, 3, 4, 5]

@api.get("/data")
def get_data(index):
    try:
        return {
            "data": data[int(index)]
        }
    except IndexError:
        raise HTTPException(
            status_code = 404,
            detail = "Unknown Index"
        )
    except ValueError:
        raise HTTPException(
            status_code = 400,
            detail = "Bad Type"
        )
