from fastapi import FastAPI


api = FastAPI(
    title = "My API"
)

@api.get("/")
def get_index():
    return { 
        "data": "Hello World"
    }

@api.get("/item/{itemid:int}")
def get_item(itemid):
    return {
        "route": "dynamic",
        "itemid": itemid
    }

@api.get("/item/{itemid}/description/{language}")
def get_item_language(itemid, language):
    if language == "en":
        return {
            "itemid": itemid,
            "description": "an object",
            "language": "en"
        }
    else:
        return {
            "itemid": itemid,
            "description": "u objet",
            "language": "fr"
        }

@api.get("/item/{itemid:float}")
def get_item_float(itemid):
    return {
        "route": "dynamic",
        "itemid": itemid,
        "source": "float"
    }

@api.get("/item/{itemid}")
def get_item_default(itemid):
    return {
        "route": "dynamic",
        "itemid": itemid,
        "source": "string"
    }
