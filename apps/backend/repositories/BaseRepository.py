from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel

from domain.models.base import Base
from motor.motor_asyncio import AsyncIOMotorDatabase


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        collection_name: str,
        model: Type[T],
        use_cache: bool = False,
    ):
        self.db = db
        self.collection = db[collection_name]
        self.model = model
        self.use_cache = use_cache

    # -------------------------------------------------------------
    async def create(self, obj: T) -> T:
        data = obj.model_dump()
        data["created_date"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        data["is_deleted"] = False

        await self.collection.insert_one(data)

        return self.model(**data)

    # -------------------------------------------------------------
    async def get_by_id(self, entity_id: str, id_key: str) -> Optional[T]:
        document = await self.collection.find_one(
            {id_key: entity_id, "is_deleted": False}
        )
        if not document:
            return None

        obj = self.model(**document)

        return obj

    # -------------------------------------------------------------
    async def get_by_filters(
        self,
        filters: BaseModel,
        skip: int = 0,
        limit: int = 100,
        date_field: str = "created_date",
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> Tuple[List[T], int, int, int]:

        query: Dict[str, Any] = {"is_deleted": False}

        filter_dict = filters.model_dump(exclude_unset=True)
        for field, value in filter_dict.items():
            if value is not None:
                query[field] = value

        if start_time or end_time:
            query[date_field] = {}
            if start_time:
                query[date_field]["$gte"] = start_time
            if end_time:
                query[date_field]["$lte"] = end_time

        cursor = (
            self.collection.find(query).skip(skip).limit(limit).sort(date_field, -1)
        )

        results = [self.model(**doc) async for doc in cursor]

        return results, len(results), skip + 1, limit

    # -------------------------------------------------------------
    async def update(
        self, id_key: str, entity_id: str, updates: Dict[str, Any]
    ) -> Optional[T]:
        valid_updates = {k: v for k, v in updates.items() if v is not None}

        if not valid_updates:
            return None

        valid_updates["updated_at"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            {id_key: entity_id, "is_deleted": False},
            {"$set": valid_updates},
            return_document=True,
        )

        if not result:
            return None

        return self.model(**result)

    # -------------------------------------------------------------
    async def delete(self, id_key: str, entity_id: str) -> bool:
        result = await self.collection.update_one(
            {id_key: entity_id, "is_deleted": False},
            {"$set": {"is_deleted": True, "updated_at": datetime.utcnow()}},
        )

        return result.modified_count > 0

    # -------------------------------------------------------------
    async def hard_delete(self, id_key: str, entity_id: str) -> bool:
        result = await self.collection.delete_one({id_key: entity_id})

        return result.deleted_count > 0
