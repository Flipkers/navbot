import aiosqlite

async def init_db():
    async with aiosqlite.connect('links.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL
            )
        ''')
        await db.commit()

if __name__ == '__main__':
    import asyncio
    asyncio.run(init_db()) 