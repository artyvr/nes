from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager
from config.settings import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False
)

@asynccontextmanager
async def get_db_session():
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()