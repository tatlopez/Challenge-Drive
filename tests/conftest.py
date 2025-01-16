import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import Session, init_db
import pytest

@pytest.fixture
def db():
    #Crea una base de datos en memoria para los tests
    init_db() 
    session = Session()  
    yield session
    session.close()  
