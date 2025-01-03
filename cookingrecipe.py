from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path

from schemas import Recipe, RecipeCreate, RecipeSearchResults
from recipe_data import RECIPES
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH/"templates"))

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

api_router = APIRouter()
#APIRouter is how we can group our API endpoints


@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """Root Get"""
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": RECIPES},
    )

@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe) #cury braces indicate the parameter value , whic needs to match one of the arguments taken by the endpoint function
def fetch_recipe(*, recipe_id: int) -> dict: #{recipe_id} is a URL path parameter. The value of recipe_id is captured from the URL.
    """Fetch a recipe"""
    print(type(recipe_id))
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe {recipe_id} not found"
        )
    return result[0]
    
# @api_router.get("/search/", status_code=200)
# def search_recipe(keyword: Optional[str] = None, max_results: Optional[int] = 10) -> dict: #The Optional type hint is a shorthand for Union[str, None], meaning the value can either be a str or None.
#     """Search for a recipe based on label keyword"""
#     if not keyword:
#         return {"results": RECIPES[:max_results]}

#     results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
#     return {"results": list(results)[:max_results]}
@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipe(*, keyword: Optional[str] = Query(
    None, min_length = 3, 
    openapi_examples={
        "PastaExample": {
            "summary": " A Pasta Search example",
            "value": "",
        }
    },
),
    max_results: Optional[int] = 10) -> dict:
    """Search for a recipe based on label keyword"""
    if not keyword:
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)        
    return {"results": list(results)[:max_results]}



@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*,recipe_in: RecipeCreate) -> dict: #As we have the pydantic schema specified, we can automatically validate incoming requests
    """Create a new recipe"""
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id = new_entry_id,
        label = recipe_in.label,
        source = recipe_in.source,
        url = recipe_in.url,
        
    )
    RECIPES.append(recipe_entry,dict())
    return recipe_entry

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port=8001, log_level = "debug")