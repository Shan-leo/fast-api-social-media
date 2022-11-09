from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Coolipso2022@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Coolipso2022',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected successfully")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(2)

