import time
import aiosqlite

from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS replied_users (
                user_id     INTEGER PRIMARY KEY,
                first_name  TEXT,
                group_id    INTEGER,
                replied_at  INTEGER
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS groups (
                group_id  INTEGER PRIMARY KEY,
                title     TEXT,
                added_at  INTEGER,
                active    INTEGER DEFAULT 1
            )
            """
        )
        await db.commit()


async def has_replied(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM replied_users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        return row is not None


async def log_reply(user_id: int, first_name: str, group_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO replied_users (user_id, first_name, group_id, replied_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, first_name, group_id, int(time.time())),
        )
        await db.commit()


async def add_group(group_id: int, title: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO groups (group_id, title, added_at, active)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(group_id) DO UPDATE SET active = 1, title = excluded.title
            """,
            (group_id, title, int(time.time())),
        )
        await db.commit()


async def deactivate_group(group_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE groups SET active = 0 WHERE group_id = ?", (group_id,)
        )
        await db.commit()


async def get_stats() -> dict:
    now = int(time.time())
    week_ago = now - 7 * 24 * 3600
    month_ago = now - 30 * 24 * 3600

    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM replied_users")
        total_users = (await cur.fetchone())[0]

        cur = await db.execute("SELECT COUNT(*) FROM groups WHERE active = 1")
        total_groups = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM replied_users WHERE replied_at >= ?", (week_ago,)
        )
        weekly_users = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM replied_users WHERE replied_at >= ?", (month_ago,)
        )
        monthly_users = (await cur.fetchone())[0]

    return {
        "total_users": total_users,
        "total_groups": total_groups,
        "weekly_users": weekly_users,
        "monthly_users": monthly_users,
    }
