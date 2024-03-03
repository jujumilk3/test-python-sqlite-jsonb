from sqlalchemy import create_engine


db_url = "sqlite:///:memory:"
# create engine
engine = create_engine(db_url)

print(engine)
