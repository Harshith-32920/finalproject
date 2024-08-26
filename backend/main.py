from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint: Returns a welcome message
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Greeting endpoint: Returns a greeting message with path parameters
@app.get("/greet/{time_of_day}/{name}")
def read_path_params(time_of_day: str, name: str):
    return {"message": f"Good {time_of_day}, {name}!"}

# Greeting endpoint: Returns a greeting message with query parameters
@app.get("/greet")
def read_query_params(time_of_day: str, name: str):
    return {"message": f"Good {time_of_day}, {name}!"}


# Database model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic models for request/response
class ItemCreate(BaseModel):
    title: str
    description: str

class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True


# Create an item: Adds a new item to the database
@app.post("/items/")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

# Read all items: Retrieves all items from the database
@app.get("/items/")
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

# Read a single item: Retrieves a specific item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update an item: Modifies an existing item by ID
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

# Delete an item: Removes an item from the database by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    db.close()
    return {"ok": True}

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
