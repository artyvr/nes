
from database.session import get_db_session
from sqlalchemy import text

async def test_async_connection() -> bool:
    try:
        async with get_db_session() as session:
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"✅ Подключение к базе успешно: {value}")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False