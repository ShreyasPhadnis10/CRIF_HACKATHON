import asyncpg
from driver import Driver

class PostgresDriver(Driver):
    async def connect(self, **kwargs):
        self.identifier = "postgres"
        connection_uri = kwargs["connection_uri"]
        max_size = kwargs["max_size"]
        min_size = kwargs["min_size"]

        pool = await asyncpg.create_pool(
            connection_uri,
            min_size=min_size,
            max_size=max_size
        )

        self._connection = pool

        async with self._connection.acquire() as conn:
            query = (
                "CREATE TABLE IF NOT EXISTS articles("
                "id SERIAL PRIMARY KEY,"
                "company_name TEXT,"
                "title TEXT,"
                "link TEXT,"
                "url TEXT,"
                "date TIMESTAMP,"
                ")"
            )
            await conn.execute(query)
        return self._connection

    async def insert(self, articles):
        async with self._connection.acquire() as conn:
            query = (
                "INSERT INTO articles (company_name, title, link, url, date)"
                "VALUES ($1, $2, $3, $4, $5)"
            )
            await conn.executemany(query, articles)

    async def fetch_processed(self, company_name: str):
        async with self._connection.acquire() as conn:
            query = (
                "SELECT  FROM articles WHERE company_name = $1"
            )
            return await conn.fetch(query, company_name)



    async def cleanup(self):
        await self._connection.close()

