from fastapi import APIRouter

router = APIRouter(tags=["work with users"], prefix="/api")


# TODO: remove route
@router.get("/")
def basic_route():
    return "basa"
