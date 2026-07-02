from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE = "todo.db"

SQL_DATABASE_URL = f"sqlite:///{DATABASE}"

engine = create_engine(
    SQL_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal class ta ekta database session create kore, ja amra CRUD operations er jonno use korbo.
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# declarative_base() function ta ekta base class create kore, ja amra amader models er jonno use korbo. Eita SQLAlchemy er ORM er ekta part, ja amader ke database table gulo ke Python class hishebe represent korte help kore.
Base = declarative_base()

# get_db function ta ekta dependency function, ja amra FastAPI er route functions e use korbo. Eita ekta database session return kore, ja amader CRUD operations er jonno dorkar. Eita ekta generator function, ja session create kore, yield kore, and finally session close kore.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()