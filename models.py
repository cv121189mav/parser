import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

from settings import DATABASE_URL

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String)
    parent = db.Column(db.Integer, db.ForeignKey('category.id'))


if __name__ == '__main__':
    from sqlalchemy import create_engine

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
