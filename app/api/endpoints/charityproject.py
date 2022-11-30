from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
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
    await check_name_duplicate(charity_project.name, session)
    project_id = await charity_project_crud.get_project_id_by_name(charity_project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Такой проект уже существует!",
        )
    new_charity_project = await charity_project_crud.create(charity_project, session)
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
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_project_crud.update(
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
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects 


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(charity_project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Такой проект уже существует!',
        ) 

@router.delete(
    '/{project_id}',
    response_model=CharityProjectRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # Выносим повторяющийся код в отдельную корутину.
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_charity_project_by_id(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project 
