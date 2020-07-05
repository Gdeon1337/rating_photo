from typing import Union

import argon2

from .trace import run_in_executor


class AsyncPasswordHasher(argon2.PasswordHasher):
    async def async_hash(self, password: Union[str, bytes]) -> str:
        return await run_in_executor(self.hash, password)

    async def async_verify(self, password_hash: Union[str, bytes], password: Union[str, bytes]) -> bool:
        try:
            return await run_in_executor(self.verify, password_hash, password)
        except argon2.exceptions.Argon2Error:
            pass
        return False

    async def async_check_needs_rehash(self, password_hash: Union[str, bytes]) -> bool:
        try:
            return await run_in_executor(self.check_needs_rehash, password_hash)
        except argon2.exceptions.Argon2Error:
            pass
        return False
