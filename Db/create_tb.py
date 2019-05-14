from Db.db_connect import Base
from Db.db_connect import engine

Base.metadata.create_all(engine)
