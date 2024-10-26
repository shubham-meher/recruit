from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Sample data
recepie = [
    {
        "id": 1,
        "title": "Chicken Curry",
        "making_time": "45 min",
        "serves": "4 people",
        "ingredients": "onion, chicken, seasoning",
        "cost": 1000,
        "created_at": "2016-01-10 12:10:12",
        "updated_at": "2016-01-10 12:10:12"
    },
    {
        "id": 2,
        "title": "Rice Omelette",
        "making_time": "30 min",
        "serves": "2 people",
        "ingredients": "onion, egg, seasoning, soy sauce",
        "cost": 700,
        "created_at": "2016-01-11 13:10:12",
        "updated_at": "2016-01-11 13:10:12"
    }
]

# Request models
class Input(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int

class UpdateInput(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int

# ID counter for new recipes
current_id = 3

# Get all recipes
@app.get("/recipes")
def get_recipes():
    return {"recipes": recepie}

# Create a new recipe
@app.post("/recipes")
def create_recipe(inp: Input):
    global current_id
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert pydantic model to dictionary and add additional fields
    new_recipe = inp.dict()
    new_recipe["id"] = current_id
    new_recipe["created_at"] = current_timestamp
    new_recipe["updated_at"] = current_timestamp
    
    recepie.append(new_recipe)
    current_id += 1
    
    return {
        "message": "Recipe successfully created!",
        "recipe": [new_recipe]
    }

# Get a recipe by ID
@app.get("/recipe/{id}")
def get_recipe_by_id(id: int = Path(...)):
    for recipe in recepie:
        if recipe["id"] == id:
            return {
                "message": "Recipe details by ID",
                "recipe": [recipe]
            }
    raise HTTPException(status_code=404, detail="Recipe not found")

# Update a recipe by ID
@app.patch("/recipe/{id}")
def update_recipe(upd: UpdateInput, id: int = Path(...)):
    for recipe in recepie:
        if recipe["id"] == id:
            recipe["title"] = upd.title
            recipe["making_time"] = upd.making_time
            recipe["serves"] = upd.serves
            recipe["ingredients"] = upd.ingredients
            recipe["cost"] = upd.cost
            recipe["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "message": "Recipe successfully updated",
                "recipe": [recipe]
            }
    raise HTTPException(status_code=404, detail="Recipe not found")