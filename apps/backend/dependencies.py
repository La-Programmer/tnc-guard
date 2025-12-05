from typing import Generator

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from repositories.ReportRepository import ReportRepository
from database import get_db


# Database Dependencies
def get_db_dependency() -> Generator[AsyncIOMotorDatabase, None, None]:
    db = get_db()
    try:
        yield db
    finally:
        pass


# Repository Dependencies
def get_report_repo(
    db: AsyncIOMotorDatabase = Depends(get_db_dependency),
) -> ReportRepository:
    return ReportRepository(db)
