from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from config.settings import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    connect_args={
        'timeout': 30,
        'check_same_thread': False,
    }
)

async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_db_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
