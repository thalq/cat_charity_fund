from app.core.db import get_async_session
from app.crud.charityproject import (create_charity_project,
                                     get_charity_project_by_id,
                                     get_project_id_by_name,
                                     read_all_projects_from_db,
                                     update_charity_project)
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectRoomDB,
                                        CharityProjectUpdate)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    project_id = await get_project_id_by_name(charity_project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Такой проект уже существует!",
        )
    new_charity_project = await create_charity_project(charity_project, session)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await get_charity_project_by_id(
        project_id, session
    )

    if charity_project is None:
        raise HTTPException(
            status_code=404, 
            detail='Проект не найден!'
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await update_charity_project(
        charity_project, obj_in, session
    )
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectRoomDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await read_all_projects_from_db(session)
    return all_projects 


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(charity_project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Такой проект уже существует!',
        ) 

