import aiosqlite

async def create_tables():
    async with aiosqlite.connect('db/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                category TEXT,
                size TEXT,
                price TEXT,
                article TEXT,
                photo TEXT
            );
        ''')
        await conn.commit()

async def insert_product(product_name, category, size, price, article, photo):
    async with aiosqlite.connect('db/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            INSERT INTO products (product_name, category, size, price, article, photo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_name, category, size, price, article, photo))
        await conn.commit()

async def fetch_all_products():
    async with aiosqlite.connect('db/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT * FROM products')
        return await cursor.fetchall()

async def fetch_product_by_id(product_id):
    async with aiosqlite.connect('db/store.sqlite3') as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return await cursor.fetchone()
