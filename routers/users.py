from fastapi import Body, APIRouter, HTTPException, Depends
from routers import items
from pydantic import BaseModel
from typing import Annotated

from models import Users,Items
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user": "Can't find user"}},
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


class User(BaseModel):
    admin: bool
    username: str
    password: str

class ItemRequest(BaseModel):
    name: str
    quantity: int

@router.put("/purchase/{user_type}")
async def purchase(admin: bool, purchase_item: ItemRequest, db:db_dependency):
    try:
        if not admin:
            items_model=db.query(Items).filter(Items.brand==purchase_item.name).first()
            if items_model is not None:
                items_model.brand = purchase_item.name
                items_model.quantity -= purchase_item.quantity

                db.add(items_model)
                db.commit()
                return {"message":f"Item {items_model.brand} has been purchased - Quantity: {purchase_item.quantity}"}
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        else:
            HTTPException(status_code=404, detail="Item can't be purchased by this user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/restock/{user_type}")
async def restock(admin: bool, restock_item: ItemRequest, db:db_dependency):
    try:
        if admin:
            items_model=db.query(Items).filter(Items.brand==restock_item.name).first()
            if items_model is not None:
                items_model.brand = restock_item.name
                items_model.quantity += restock_item.quantity

                db.add(items_model)
                db.commit()
                return {"message":f"Item {items_model.brand} has been restocked - Current quantity: {items_model.quantity}"}
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        else:
            HTTPException(status_code=404, detail="Item can't be restocked by this user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/total-revenue/{brand}")
async def total_revenue(admin: bool, brand: str, db:db_dependency):
    try:
        if admin:
            items_model=db.query(Items).filter(Items.brand==brand).first()
            if items_model is not None:
                quantity_difference=20-items_model.quantity
                total = quantity_difference * items_model.price
                return {"message":f"Items {items_model.brand} total revenue - {total} KM"}
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        else:
            HTTPException(status_code=404, detail="Total revenue can't be seen by this user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
