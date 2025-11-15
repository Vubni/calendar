from database.database import Database

async def init_db():
    async with Database() as db:
        try:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS public.events
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( START 1 MINVALUE 1 MAXVALUE 999999999999999 CACHE 1 ),
    title character varying(80) NOT NULL,
    date date NOT NULL,
    time_start timestamp with time zone NOT NULL,
    time_stop timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);""")
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")