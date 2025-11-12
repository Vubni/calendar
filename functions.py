from database.database import Database
from datetime import datetime, date
from config import logger

async def insert_mero(title:str, description:str, date:date, time_start:str, time_stop:str):
    try:
        async with Database() as db:
            await db.execute("INSERT INTO events (title, description, date, time_start, time_stop), ($1, $2, $3, $4, $5)",
                            (title, description, date, time_start, time_stop))
        return True
    except Exception as e:
        logger.error(str(e))
        return False

async def get_mero():
    try:
        async with Database() as db:
            return await db.execute_all("SELECT id, title, date, time_start, time_stop FROM events")
        return True
    except Exception as e:
        logger.error(str(e))
        return False
    
async def get_mero_info(id:int):
    try:
        async with Database() as db:
            return await db.execute_all("SELECT * FROM events WHERE id=$1", (id,))
        return True
    except Exception as e:
        logger.error(str(e))
        return False
    
async def del_mero(id:int):
    try:
        async with Database() as db:
            await db.execute("DELETE FROM events WHERE id=$1", (id,))
        return True
    except Exception as e:
        logger.error(str(e))
        return False

async def edit_mero(id:int, title:str="", description:str=""):
    try:
        async with Database() as db:
            if title:
                await db.execute("UPDATE events SET title=$1 WHERE id=$2", (title, id))
            elif description:
                await db.execute("UPDATE events SET description=$1 WHERE id=$2", (description, id))
        return True
    except Exception as e:
        logger.error(str(e))
        return False