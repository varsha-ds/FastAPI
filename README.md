URL Path Parameters: Dynamic segments in the URL used to capture data like recipe_id in /recipe/{recipe_id}.
Type Hints: Python annotations to specify expected types of function parameters and return values, like Optional[str] and Optional[int].
Query Parameters: Key-value pairs passed in the URL after ?, used for filtering, sorting, or setting options, like ?keyword=pasta&max_results=5.
HTTP Status code 201- for creating resources
To set the function to handle POST requests - we make modifications to api_router decorator

Query: Used for query parameter validation, setting additional constraints like minimum length, and generating OpenAPI documentation.
HTTPException: Used to raise custom HTTP errors with status codes and error details.

from schemas import Recipe, RecipeCreate, RecipeSearchResults:
These are Pydantic schemas for input validation and serialization. They define how data should be structured for various endpoints.

keyword: Optional[str] = Query(None, min_length=3): The keyword query parameter is optional and must be at least 3 characters long. If no keyword is provided, it defaults to None.
openapi_examples: This is an additional feature that provides examples for the OpenAPI documentation. It specifies an example keyword ("chicken") that can be used in the documentation.
max_results: Optional[int] = 10: Limits the number of results returned to 10 by default.

##Structure and Flow:##
FastAPI app is initialized.
Router (APIRouter) is used to group API endpoints, which are then included in the main FastAPI app.
Each endpoint handles a specific recipe-related operation:
Root endpoint: Returns a greeting message.
Fetch recipe by ID: Retrieves a recipe using a URL path parameter (recipe_id).
Search recipes: Allows searching recipes based on a keyword and limiting the number of results.
Create recipe: Accepts a POST request to create a new recipe.