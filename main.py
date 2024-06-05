from fastapi import FastAPI
import uvicorn
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/", description="App get decription", deprecated=False)
async def root():
    return {"message": "Hello world"}

@app.put("/")
async def put():
    return {"message": "Hello world from put route"}

@app.post("/")  
async def post():
    return {"message": "Hello world from post route"}

@app.get("/users") # path parameter diye geçen kısım. URL'nin sonuna yazılıp görüntülenebiliyor. localhost:8080/users gibi
async def list_users():
    return {"message": "List users"}

@app.get("/users/me") # statik ve dinamik iki adet endpoint bulunuyor ve ilk olarak statiğe bakılması isteniyorsa, statik olan endpoint üste konulmalı.
async def get_current_user():
    return {"message":"this is the current user"}

@app.get("/users/{user_id}")
async def get_item(user_id : int): # int ataması, item_id'nin hangi data tipinde gösterilecegini belirliyor
    return {"User ID":user_id} # bu kısımda item_id string olarak gösteriliyor. Bunun önüne geçmek için bir üst satırda int ataması yapılabilir

class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name = FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message":"you are healthy"}
    
    if food_name.value == "fruits":
        return {"food_name":food_name, "message":"you are still healthy with friuts"}

    return {"food_name":food_name, "message":"Dairy selected, healthy"}


fake_items_db = [{"item_name":"Foo"}, 
                 {"item_name":"Bar"}, 
                 {"item_name":"Sully"}]


@app.get("/items")
async def list_items(skip: int = 0, limit:int = 10): # query parameters örneği
    return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}") # bu kısım http://localhost:8000/items/hello?q=world&short=1 şeklinde browser üzerinde kullanılabilir
async def get_item(item_id: str, q: Optional[str] = None, short : bool = False):
    item = {"item_id":item_id}

    if q:
        item.update({"q":q})
    if not short:
        item.update({"description":"Description section with some words"})
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    # query parametreleri, fonksiyonda parametre olarak bulunan fakat route pathinde bulunmayan parametreler için kullanılır.
    item = {"item_id":item_id, "owner_id":user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description":"Description section with some words"})
    return item



class Item(BaseModel):
    name :str
    description: Optional[str] = None # description değişkeni burda optional, girilmediği durumda None değer olacak. Python 3.10 ve üzeri için bu kısım str | None = None şeklinde de yazılabilir.
    price: float
    tax: Optional[float] = None


@app.post("/items")
async def create_item(item : Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id : int, item: Item, q: Optional[str] = None):
    result = {"item_id":item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)