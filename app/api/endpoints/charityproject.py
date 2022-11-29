from fastapi import APIRouter, HTTPException

from app.crud.charityproject import create_charity_project, get_project_id_by_name
from app.schemas.charityproject import CharityProjectCreate, CharityProjectRoomDB

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectRoomDB,
)
async def create_new_meeting_room(
    charity_project: CharityProjectCreate,
):
    project_id = await get_project_id_by_name(charity_project.name)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Такой проект уже существует!",
        )
    new_charity_project = await create_charity_project(charity_project)
    return new_charity_project
