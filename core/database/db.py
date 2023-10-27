from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import db_string


class DatabaseConnector:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_engine(url=url, echo=echo)
        self.session = sessionmaker(bind=self.engine, expire_on_commit=False)


db = DatabaseConnector(url=db_string, echo=True)

# from core.database.models import Base

# with db.session.begin():
#   Base.metadata.drop_all(db.engine)
#   Base.metadata.create_all(db.engine)
