from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy import create_engine, DateTime, String, TypeDecorator, func, JSON


db_url = "sqlite:///:memory:"
# create engine
engine = create_engine(db_url)

print(engine)

metadata_obj = sqlalchemy.MetaData()


class BaseSqlalchemyModel(DeclarativeBase):
    metadata = metadata_obj

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

    # def __repr__(self):
    #     return f"<{self.__class__.__name__} id={self.id}>"


class TestModel(BaseSqlalchemyModel):
    name = mapped_column(String(255), nullable=False)
    data = mapped_column(JSON)


# create tables
# BaseSqlalchemyModel.metadata.create_all(engine)
# metadata.create_all(engine)

metadata_obj.create_all(engine)

# check table
testmodel = TestModel(name="test", data={"key": "value"})
print(testmodel)
# add to session
test_model_id = None
with sqlalchemy.orm.Session(engine) as session:
    session.add(testmodel)
    session.commit()
    print(testmodel.id)
    test_model_id = testmodel.id


# select by id
print("select by id")
with sqlalchemy.orm.Session(engine) as session:
    testmodel = session.query(TestModel).get(test_model_id)
    print(testmodel)
    print(testmodel.id)
    print(testmodel.name)
    print(testmodel.data)  # {'key': 'value'}
    print(type(testmodel.data))  # <class 'dict'>
    print(testmodel.created_at)
    print(testmodel.updated_at)
