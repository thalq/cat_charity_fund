# app/crud/meeting_room.py

# Импортируем sessionmaker из файла с настройками БД.
from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate


async def create_charity_project(
    charity_project: CharityProjectCreate,
) -> CharityProject:
    new_charity_project = charity_project.dict()
    db_project = CharityProject(**new_charity_project)

    async with AsyncSessionLocal() as session:
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(project_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        project_id = project_id.scalars().first()
    return project_id
