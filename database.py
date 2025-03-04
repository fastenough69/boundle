import aiosqlite
import asyncio
import bcrypt

class DataBaseUsers:
    def __init__(self, file_db: str) -> None:
        self.file_db = file_db

    async def __verify_password(self, stored_password: bytes, provided_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    async def create_table(self):
        async with aiosqlite.connect(self.file_db) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS requests '
                            '(user_id INTEGER, password BLOB, status VARCHAR DEFAULT "deactivate")')
            await db.commit()

    async def __hashed_string(self, password: str):
        salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return pass_hash

    async def new_user(self, user_id: int, password: str):
        async with aiosqlite.connect(self.file_db) as db:
            cursor = await db.execute('SELECT user_id FROM requests WHERE user_id = ?', (user_id,))
            exicting = await cursor.fetchone()
            if exicting:
                return
            
            hash_pass = await self.__hashed_string(password)
            await db.execute('INSERT INTO requests (user_id, password) VALUES (?, ?)', 
                            (user_id, hash_pass))
            await db.commit()

    async def check_user(self, user_id: int, password: str):
        async with aiosqlite.connect(self.file_db) as db:
            cursor = await db.execute('SELECT password FROM requests WHERE user_id = ?', (user_id,))
            existing = await cursor.fetchone()
            if existing:
                _password = existing[0]
                if await self.__verify_password(_password, password):
                    return True
                else:
                    return False
            else:
                return

    async def set_status(self, user_id: int):
        async with aiosqlite.connect(self.file_db) as db:
            status = 'activate'
            cursor = await db.execute('SELECT status FROM requests WHERE user_id = ?', (user_id,))
            exicting = await cursor.fetchone()
            if exicting:
                await db.execute('UPDATE requests SET status=?', 
                            (status,))
                await db.commit()

    async def get_status(self, user_id: int):
        async with aiosqlite.connect(self.file_db) as db:
            cursor = await db.execute('SELECT status FROM requests WHERE user_id = ?', (user_id,))
            existing = await cursor.fetchone()
            result = False
            if existing[0] == 'activate':
                result = True
            return result
                
    
# async def main():
#     name = 'users.db'
#     db = DataBaseUsers(name)
#     await db.create_table()
#     await db.new_user(1482790150, '12345')
#     await db.new_user(6367438515, 'qweyainvoker228')
#     await db.new_user(5525988316, '892016')
#     # await db.set_status(1482790150)
#     # await db.get_status(1482790150)

# if __name__ == '__main__':
#     asyncio.run(main())