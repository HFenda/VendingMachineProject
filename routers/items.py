from fastapi import APIRouter, HTTPException, Depends,Path
from pydantic import BaseModel, Field
from typing import Optional, List
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Items

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={401: {"item": "Not found"}}
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


class Item(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=30)
    brand: str = Field(min_length=3, max_length=30)
    price: float = Field(gt=0)
    quantity: int = Field(gt=-1, lt=21)


def find_item_id():
    if ITEMS:
        id = ITEMS[-1].id + 1
    else:
        id = 1
    return id

@router.get("/all-items")
async def get_all_items(db:db_dependency):
    try:
        return db.query(Items).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/{item_id}")
async def get_item_by_brand(db:db_dependency ,item_id: str):
    try:
        items_model=db.query(Items).filter(Items.id==item_id).first()
        if items_model is not None:
            return items_model
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-item")
async def create_item(db: db_dependency ,item_request: Item):
    try:
        items_model=Items(**item_request.dict())
        db.add(items_model)
        db.commit()
        return items_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-item/{item_id}")
async def update_item(db:db_dependency,
                      item_request: Item,
                      item_id: int=Path(gt=0)):
    try:
        items_model=db.query(Items).filter(Items.id==item_id).first()
        if items_model is not None:
            items_model.title= item_request.title
            items_model.brand= item_request.brand
            items_model.price= item_request.price
            items_model.quantity= item_request.quantity

            db.add(items_model)
            db.commit()
            return items_model
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-item/{item_id}")
async def delete_item(db:db_dependency, item_id: int=Path(gt=0)):
    try:
        items_model=db.query(Items).filter(Items.id==item_id).first()
        if items_model is not None:
            db.delete(items_model)
            db.commit()
            return items_model
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except:
        raise HTTPException(status_code=404, detail="Item not found")
