import os
import asyncio
from database import db, Photo


async def main():
    photo_path = 'путь до папки с фотками'
    photos = os.listdir(photo_path)
    for photo in photos:
        await Photo.create(path=f'{photo_path}/{photo}')


asyncio.run(main())
