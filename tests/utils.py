from typing import List

from app.extensions import conn


async def create_domains(domains: List, timestamp: int):
    await conn.zadd(domains, timestamp)
