from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete, func, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression

from app.core.base_class import AsyncBase

ModelType = TypeVar("ModelType", bound=AsyncBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression,
    ) -> Optional[ModelType]:
        res = await db.execute(select(self.model).where(filter_expr))
        return res.scalars().one_or_none()

    async def exists_or_404(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression,
    ) -> Optional[ModelType]:
        res = await db.execute(select(self.model.id).where(filter_expr))
        db_obj = res.scalars().one_or_none()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Object is not found")
        return db_obj

    async def raise_if_exists(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression,
        name: str,
    ) -> Optional[ModelType]:
        res = await db.execute(select(self.model.id).where(filter_expr))
        db_obj = res.scalars().one_or_none()
        if db_obj is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{name} exists")
        return db_obj

    async def get_multi(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression = None,
        skip: int = 0,
        limit: int = 100,
        order: str = None,
    ) -> List[ModelType]:

        select_st = select(self.model)
        if filter_expr is not None:
            select_st = select_st.where(filter_expr)

        if order is not None:
            select_st = select_st.order_by(order)

        if skip is not None:
            select_st = select_st.offset(skip)

        if limit is not None:
            select_st = select_st.limit(limit)

        res = await db.execute(select_st)
        return res.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        update_st = update(self.model).where(filter_expr).values(**obj_in.model_dump())
        await db.execute(update_st)
        await db.commit()
        return await self.get(db, filter_expr)

    async def remove(self, db: AsyncSession, filter_expr: BinaryExpression) -> None:
        await db.execute(delete(self.model).where(filter_expr))
        await db.commit()
        return

    async def bulk_remove(self, db: AsyncSession, filter_expr: BinaryExpression) -> None:
        await db.execute(delete(self.model).where(filter_expr))
        await db.commit()
        return

    async def count(self, db: AsyncSession, filter_expr: BinaryExpression = None) -> int:

        select_st = select(func.count(self.model.id))

        if filter_expr is not None:
            select_st = select_st.where(filter_expr)

        res = await db.execute(select_st)
        return res.scalar_one()

    async def bulk_create(self, db: AsyncSession, objects_in: List[CreateSchemaType]) -> None:
        await db.execute(insert(self.model), [obj.dict() for obj in objects_in])
        await db.commit()
        return
