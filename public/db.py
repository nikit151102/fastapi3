from sqlalchemy import create_engine, text, insert, select
from sqlalchemy.ext.asyncio import create_async_engine
from models.dbcontext import Base, Company
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import database_exists, create_database

ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA

engine_s = create_engine(ur_s, echo=True)
engine_a = create_async_engine(ur_a, echo=True)

async def get_session():
    async with AsyncSession(engine_a) as session:
        try:
            yield session
        finally:
            session.close()

def create_db():
     if not database_exists(engine_s.url):
            create_database(engine_s.url)

def create_tables():
     Base.metadata.drop_all(bind = engine_s)
     Base.metadata.create_all(bind = engine_s)

def index_builder():
     with engine_s.connect() as conn:
        query = insert(Company).values([
             {"name": "Ростех", "country": "Россия"},
             {"name": "Айтеко", "country": "Россия"}
        ])
        conn.execute(query)
        conn.execute(text('commit;'))
        query = select(Company)
        answer = conn.execute(query)
        print(f"answer = {answer.all()}")