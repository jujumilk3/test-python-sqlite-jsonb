from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy import DateTime, String, TypeDecorator, func, JSON


db_url = "sqlite:///:memory:"
# create engine
engine = create_engine(db_url)

print(engine)


class BaseSqlalchemyModel(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class TestModel(BaseSqlalchemyModel):
    name = mapped_column(String(255), nullable=False)
    data = mapped_column(JSON)
