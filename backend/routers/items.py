from fastapi import APIRouter, HTTPException, Depends,Path
from pydantic import BaseModel, Field
from typing import Optional, List
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func,select
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
    quantity: int = Field(ge=0, le=20)  # Changed to ge/le for better validation

    class Config:
        from_attributes = True  # Changed from orm_mode for Pydantic v2


@router.get("/all-items")
async def get_all_items(db: db_dependency):
    try:
        return db.query(Items).order_by(Items.id.asc()).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{item_id}")
async def get_item_by_brand(db: db_dependency, item_id: int = Path(gt=0)):  # Changed to expect int
    try:
        items_model = db.query(Items).filter(Items.id == item_id).first()
        if items_model is not None:
            return items_model
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-item", response_model=Item)
async def create_item(item_request: Item, db: Session = Depends(get_db)):
    try:
        existing_ids = db.query(Items.id).order_by(Items.id).all()
        existing_ids = [id_tuple[0] for id_tuple in existing_ids]

        next_id = 1
        for id in existing_ids:
            if id == next_id:
                next_id += 1
            else:
                break

        item_data = Items(id=next_id, **item_request.dict(exclude={"id"}))

        db.add(item_data)
        db.commit()
        db.refresh(item_data)
        return item_data
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
async def delete_item(db: db_dependency, item_id: int = Path(gt=0)):
    try:
        items_model = db.query(Items).filter(Items.id == item_id).first()
        if items_model is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(items_model)
        db.commit()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
