from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class DriveFile(Base):
    __tablename__ = 'drive_files'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    visibility = Column(Boolean, nullable=False)
    last_modified = Column(DateTime, nullable=False)


class PublicFileHistory(Base):
    __tablename__ = 'public_file_history'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    changed_at = Column(DateTime, nullable=False)


def get_engine():
    db_url = os.getenv('DATABASE_URL', 'sqlite:///drive_inventory.db')
    return create_engine(db_url)


def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=get_engine())