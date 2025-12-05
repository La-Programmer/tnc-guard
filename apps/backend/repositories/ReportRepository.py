from domain.models.report import Report
from repositories.BaseRepository import BaseRepository
from motor.motor_asyncio import AsyncIOMotorDatabase


class ReportRepository(BaseRepository[Report]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super.__init__(db, "report", Report)
