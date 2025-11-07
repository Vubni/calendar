from database.database import Database
from aiohttp import web

async def check_token(token):
    async with Database() as db:
        res = await db.execute("SELECT user_id FROM tokens WHERE token=$1", (token,))
        if not res:
            return web.Response(status=401, text="Invalid token")
    return int(res["user_id"])

async def init_db():
    async with Database() as db:
        try:
            # Сначала создаем таблицы без внешних ключей
            await db.execute("""
                CREATE TABLE IF NOT EXISTS public.users
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    email character varying COLLATE pg_catalog."default",
    name character varying COLLATE pg_catalog."default" NOT NULL,
    surname character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    telegram_id bigint,
    login character varying(20) COLLATE pg_catalog."default" NOT NULL,
    class_number integer NOT NULL,
    class_letter character varying(1) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)""")
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")