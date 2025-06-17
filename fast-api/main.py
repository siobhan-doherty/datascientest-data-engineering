from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


api = FastAPI()

class Item(BaseModel):
    itemid: int
    description: str
    owner: Optional[str] = None

@api.post('/item')
def post_item(item: Item):
    return item
