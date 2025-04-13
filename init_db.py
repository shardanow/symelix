import asyncio
from db.models import Base
from db.database import engine

async def init():
    async with engine.begin() as conn:
        print("⏳ Creating database schema...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Done!")

if __name__ == "__main__":
    asyncio.run(init())
