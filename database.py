import aiosqlite
from config import DATABASE_PATH

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                birth_date TEXT,
                gender TEXT,
                specialty TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                purpose TEXT,
                interests TEXT,
                experience TEXT,
                participation_type TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_user(user_data):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO users (
                user_id, full_name, birth_date, gender, specialty, address, 
                phone, email, purpose, interests, experience, participation_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data['user_id'], user_data['full_name'], user_data['birth_date'],
            user_data['gender'], user_data['specialty'], user_data['address'],
            user_data['phone'], user_data['email'], user_data['purpose'],
            user_data['interests'], user_data['experience'], user_data['participation_type']
        ))
        await db.commit()

async def update_status(user_id, status):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_all_members():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT full_name, user_id FROM users WHERE status = 'approved'") as cursor:
            return await cursor.fetchall()

async def get_pending_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE status = 'pending'") as cursor:
            return await cursor.fetchall()

async def delete_user(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()
