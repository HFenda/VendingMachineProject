from fastapi import Body, APIRouter,HTTPException
from routers import items
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user": "Can't find user"}},
)

class User:
    type: str
    username: str
    password: str

    def __init__(self, type: str, username: str, password: str):
        self.type = type
        self.username = username
        self.password = password

USERS=[
    User( "admin",  "admin1",  "admin1"),
    User( "user", "user1",  "user1")
]



class ItemRequest(BaseModel):
    name: str
    quantity: int

@router.post("/purchase/{user_type}")
async def purchase(user_type: str, purchase_item: ItemRequest):
    if user_type=="user":
        for item in items.ITEMS:
            if item.brand.casefold()==purchase_item.name.casefold():
                if item.quantity >= purchase_item.quantity:
                    item.quantity -=purchase_item.quantity
                    return {"message": "Item has been purchased"}
                raise HTTPException(status_code=400, detail="Not enough stock available")
    raise HTTPException(status_code=400, detail="That user can't purchase items")

@router.post("/restock/{user_type}")
async def purchase(user_type: str, restock_item: ItemRequest):
    if user_type=="admin":
        for item in items.ITEMS:
            if item.brand.casefold()==restock_item.name.casefold():
                if item.quantity < 20:
                    item.quantity +=restock_item.quantity
                    return {"message": "Item has been successfully restocked"}
                raise HTTPException(status_code=400, detail="Not enough stock available")
    raise HTTPException(status_code=400, detail="That user can't restock items")

@router.get("/total-revenue/{user_type}/{brand}")
async def total_revenue(user_type: str, brand: str):
    if user_type=="admin":
        for item in items.ITEMS:
            if item.brand.casefold()==brand.casefold():
                return (20-item.quantity)*item.price
    raise HTTPException(status_code=400, detail="You don't have access to those information")