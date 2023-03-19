from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, String, Date
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base

from app.core import config

connstr = "postgresql://%s:%s@%s/%s" % (
    config.POSTGRES_USER,
    config.POSTGRES_PASSWORD,
    config.POSTGRES_SERVER,
    config.POSTGRES_DB,
)
engine = create_engine(connstr)

Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def setup_db():
    print("running setup_db")
    with Session() as session:
        create_table_sql = text(
            """CREATE TABLE IF NOT EXISTS
                users(
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    date_of_birth DATE NOT NULL);
              """
        )

        session.execute(create_table_sql)
        session.commit()


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    date_of_birth = Column(Date)
