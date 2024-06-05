from fastapi import Body, APIRouter, HTTPException
from pydantic import BaseModel,Field
from typing import Optional

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={401: {"item": "Not found"}}
)


class Item:
    id: int
    title: str
    brand: str
    price: float
    quantity: int

    def __init__(self, id: int, title: str, brand: str, price: float, quantity: int):
        self.id = id
        self.title = title
        self.brand = brand
        self.price = price
        self.quantity = quantity

class ItemRequest(BaseModel):
    id: Optional[int]=None
    title: str =Field(min_length=3, max_length=30)
    brand: str = Field(min_length=3, max_length=30)
    price: float = Field(gt=0)
    quantity: int = Field(gt=-1, lt=21)

ITEMS=[
    Item(1,"Chocolate bar", "Dorina" , 1.5,  15),
    Item( 2,"Potato chips",  "Chio",  2.4,  8),
    Item( 3, "Soda",  "Coca-Cola",  1.2,  10),
    Item( 4, "Water", "Oaza",  0.8,  9),
    Item( 5, "Candy",  "Skittles",  1.5,  8),
    Item( 6, "Crackers",  "Tuc",  1.8,  6),
    Item( 7, "Energy drink", "Red Bull",  2.2,  8),
    Item( 8, "Ice Tea",  "Lipton", 1.0,  6)
]

def find_item_id(item: Item):
    if len(ITEMS)>0:
        item.id = ITEMS[-1].id+1
    else:
        item.id=1

    return item

@router.get("/all-items")
async def get_all_items():
    return ITEMS

@router.get("/{item_brand}")
async def get_all_items(item_brand: str):
    for item in ITEMS:
        if item.brand.casefold() == item_brand.casefold():
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/add-item")
async def create_item(item_request: ItemRequest):
    new_item=Item(**item_request.dict())
    ITEMS.append(find_item_id(new_item))

@router.put("/update-item")
async def update_item(item_request: ItemRequest):
    updated_item=Item(**item_request.dict())
    for i in range(len(ITEMS)):
        if ITEMS[i].brand.casefold() == updated_item.brand.casefold():
            ITEMS[i]= updated_item

@router.delete("/delete-item/{item_brand}")
async def delete_item(item_brand: str):
    for i in range(len(ITEMS)):
        if ITEMS[i].brand.casefold() == item_brand.casefold():
            ITEMS.pop(i)
            break