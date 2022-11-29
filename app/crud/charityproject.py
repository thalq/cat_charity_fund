# app/crud/meeting_room.py

from typing import Optional

from app.core.db import AsyncSessionLocal
from app.models.charityproject import CharityProject
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectUpdate)
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession,
) -> CharityProject:
    new_charity_project = charity_project.dict()
    db_project = CharityProject(**new_charity_project)

    async with AsyncSessionLocal() as session:
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
    project_name: str,
    session: AsyncSession,
) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        project_id = project_id.scalars().first()
    return project_id


async def get_charity_project_by_id(
        project_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    db_project = db_project.scalars().first()
    return db_project


async def update_charity_project(
        db_project: CharityProject,
        project_upd: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    obj_data = jsonable_encoder(db_project)
    update_data = project_upd.dict(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_project, field, update_data[field])
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def read_all_projects_from_db(
        session: AsyncSession,
) -> list[CharityProject]:
    db_rooms = await session.execute(select(CharityProject))
    return db_rooms.scalars().all()
