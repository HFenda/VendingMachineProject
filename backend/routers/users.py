from fastapi import Body, APIRouter, HTTPException, Depends,Query
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
    id: int
    quantity: int

class LoginRequest(BaseModel):
    username: str
    password: str

@router.put("/purchase/{user_type}")
async def purchase(
    user_type: str,
    admin: bool = Query(...),
    db: Session = Depends(get_db),  
    purchase_item: ItemRequest = Body(...)
):
    try:
        if not admin:
            items_model = db.query(Items).filter(Items.id == purchase_item.id).first()
            if items_model is not None:
                items_model.quantity -= purchase_item.quantity
                db.add(items_model)
                db.commit()
                return {"message": f"Item {items_model.brand} has been purchased - Quantity: {purchase_item.quantity}"}
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        else:
            raise HTTPException(status_code=403, detail="Item can't be purchased by this user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/total-revenue/{brand}")
async def total_revenue(
    brand: str,
    admin: bool = Query(...),
    db: Session = Depends(get_db)
):
    try:
        if admin:
            items_model = db.query(Items).filter(Items.brand == brand).first()
            if items_model is not None:
                quantity_difference = 20 - items_model.quantity
                total = quantity_difference * items_model.price
                return {"message": f"Items {items_model.brand} total revenue - {total} KM"}
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        else:
            raise HTTPException(status_code=403, detail="Total revenue can't be seen by this user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(user_credentials: LoginRequest, db: db_dependency):
    try:
        user = db.query(Users).filter(Users.username == user_credentials.username).first()

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        db_password = user.password or ""
        input_password = user_credentials.password or ""

        if db_password != input_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        role = "admin" if user.admin else "user"

        return {"message": "Login successful", "role": role}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))