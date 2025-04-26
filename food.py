from fastapi import Depends, Request, APIRouter
from httpx import AsyncClient

from config import get_id_endpoint, get_search_endpoint

router = APIRouter(prefix="/food")

@router.get("/{food_id}")
async def get_food(request: Request,
                   food_id: int,
                   endpoint: str = Depends(get_id_endpoint)) -> dict:
    client: AsyncClient = request.state.client
    params = {
        "format": "json",
        "food_id": food_id,
    }
    reponse = await client.get(endpoint, params=params)
    return reponse.json()

@router.get("")
async def search_foods(request: Request,
                       search_expression: str,
                       page_number: int = 0,
                       max_results: int = 50,
                       endpoint: str = Depends(get_search_endpoint)):
    client: AsyncClient = request.state.client
    params = {
        "format": "json",
        "search_expression": search_expression,
        "page_number": page_number,
        "max_results": max_results
    }
    reponse = await client.get(endpoint, params=params)
    return reponse.json()