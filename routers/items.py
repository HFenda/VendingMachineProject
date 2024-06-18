from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={401: {"item": "Not found"}}
)

class Item(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=30)
    brand: str = Field(min_length=3, max_length=30)
    price: float = Field(gt=0)
    quantity: int = Field(gt=-1, lt=21)

ITEMS: List[Item] = [
    Item(id=1, title="Chocolate bar", brand="Dorina", price=1.5, quantity=15),
    Item(id=2, title="Potato chips", brand="Chio", price=2.4, quantity=8),
    Item(id=3, title="Soda", brand="Coca-Cola", price=1.2, quantity=10),
    Item(id=4, title="Water", brand="Oaza", price=0.8, quantity=9),
    Item(id=5, title="Candy", brand="Skittles", price=1.5, quantity=8),
    Item(id=6, title="Crackers", brand="Tuc", price=1.8, quantity=6),
    Item(id=7, title="Energy drink", brand="Red Bull", price=2.2, quantity=8),
    Item(id=8, title="Ice Tea", brand="Lipton", price=1.0, quantity=6)
]

def find_item_id():
    if ITEMS:
        id = ITEMS[-1].id + 1
    else:
        id = 1
    return id

@router.get("/all-items")
async def get_all_items():
    return ITEMS

@router.get("/{item_brand}")
async def get_item_by_brand(item_brand: str):
    for item in ITEMS:
        if item.brand.casefold() == item_brand.casefold():
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/add-item")
async def create_item(item_request: Item):
    new_item = item_request
    new_item.id = find_item_id()
    ITEMS.append(new_item)
    return new_item

@router.put("/update-item")
async def update_item(item_request: Item):
    for i in range(len(ITEMS)):
        if ITEMS[i].id == item_request.id:
            ITEMS[i] = item_request
            return item_request
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/delete-item/{item_brand}")
async def delete_item(item_brand: str):
    for i in range(len(ITEMS)):
        if ITEMS[i].brand.casefold() == item_brand.casefold():
            return ITEMS.pop(i)
    raise HTTPException(status_code=404, detail="Item not found")