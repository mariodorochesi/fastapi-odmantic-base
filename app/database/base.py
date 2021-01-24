from typing import TypeVar, Optional
from odmantic import Model
from odmantic import AIOEngine, ObjectId


class BaseCRUD():
    """
        CRUD Object with default methos to:
            - Get object by its object_id
            - Create new record on database
            - Update existing record on database
            - Delete an existing record on database
    """

    def __init__(self, model: Model, engine: AIOEngine):
        self.model = model
        self.engine = engine

    async def get(self, id: str, engine: Optional[AIOEngine] = None) -> Optional[Model]:
        query = self.model.id == ObjectId(id)
        return await (engine.find_one(self.model, query) if engine is not None else self.engine.find_one(self.model, query))

    async def create_or_update(self, data: Model, engine: Optional[AIOEngine] = None) -> Optional[Model]:
        return await (engine.save(data) if engine is not None else self.engine.save(data))

    async def delete(self, data: Model, engine: Optional[AIOEngine] = None) -> Optional[Model]:
        return await (engine.delete(data) if engine is not None else self.engine.delete(data))
