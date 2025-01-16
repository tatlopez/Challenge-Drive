import pytest
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, DriveFile, PublicFileHistory, get_engine, Session

#configurar una base de datos en memoria para los tests
@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    
    yield session  
    
    session.close()


def test_create_drive_file(test_db):
    #Test para insertar un archivo en la base de datos.
    new_file = DriveFile(
        id="1",
        name="test_file.txt",
        extension="txt",
        owner="user@example.com",
        visibility=True,
        last_modified=datetime.strptime("2025-01-16 10:00:00", "%Y-%m-%d %H:%M:%S")
    )

    test_db.add(new_file)
    test_db.commit()

    #Verificar que el archivo se guardó correctamente
    file = test_db.query(DriveFile).filter_by(id="1").first()
    assert file is not None
    assert file.name == "test_file.txt"
    assert file.owner == "user@example.com"



def test_create_public_file_history(test_db):
    #Test para insertar un historial de archivo público.
    new_history = PublicFileHistory(
        id="1",
        name="public_file.txt",
        owner="user@example.com",
        changed_at=datetime.strptime("2025-01-16 12:00:00", "%Y-%m-%d %H:%M:%S")
    )

    test_db.add(new_history)
    test_db.commit()

    #Verificar que el historial se guardo 
    history = test_db.query(PublicFileHistory).filter_by(id="1").first()
    assert history is not None
    assert history.name == "public_file.txt"
    assert history.owner == "user@example.com"
