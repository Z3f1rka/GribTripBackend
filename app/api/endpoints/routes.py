from fastapi import APIRouter

from app.api.schemas import RouteCreateParameters
from app.api.schemas import RouteReturn
from app.api.schemas import RouteUpdateParameters

router = APIRouter(tags=["Working with map routes"], prefix="/api/routes")

"""async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService:  # noqa
    return None"""


@router.post("/create")
async def create(route: RouteCreateParameters):
    return None


@router.post("/update")
async def update(route: RouteUpdateParameters):
    return None


@router.get("/get")
async def get(route) -> RouteReturn:
    return None
