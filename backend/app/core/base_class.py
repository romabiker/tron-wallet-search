from sqlalchemy import MetaData
# from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base = DeclarativeBase(metadata=MetaData(naming_convention=convention))

class AsyncBase(AsyncAttrs, Base):
    __abstract__ = True
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
    