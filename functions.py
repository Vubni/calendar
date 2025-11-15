from database.database import Database
from datetime import datetime, date
from config import logger

async def insert_mero(title:str, date:date, time_start:str, time_stop:str):
    try:
        async with Database() as db:
            await db.execute("INSERT INTO events (title, date, time_start, time_stop) VALUES ($1, $2, $3, $4)",
                            (title, date, time_start, time_stop))
        return True
    except Exception as e:
        logger.error(str(e))
        return False

async def get_mero(date_mero:date=None, export:bool=False):
    try:
        async with Database() as db:
            if not date_mero:
                if not export:
                    return await db.execute_all("SELECT id, title, date, time_start, time_stop FROM events ORDER BY date")
                return await db.execute_all("SELECT title, date, time_start, time_stop FROM events ORDER BY date")
            return await db.execute_all("SELECT id, title, time_start, time_stop FROM events WHERE date=$1 ORDER BY time_start DESC", (date_mero,))
    except Exception as e:
        logger.error(str(e))
        return False
    
async def get_mero_info(id:int):
    try:
        async with Database() as db:
            return await db.execute_all("SELECT * FROM events WHERE id=$1", (id,))
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