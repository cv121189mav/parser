import sqlalchemy as db
from settings import DATABASE_URL


engine = db.create_engine(DATABASE_URL)
connection = engine.connect()
meta = db.MetaData(bind=connection, reflect=True)
