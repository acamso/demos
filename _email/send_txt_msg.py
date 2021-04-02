# *- coding: utf-8 -*-
# send_txt_msg.py
# 04-02-2021 03:08:34 EDT
# (c) 2021 acamso

"""Sends TXT message with GMail.

This is a demonstration on how to send an text message with Python.
In this example, we use GMail to send the SMS message,
but any host can work with the correct SMTP settings.
Each carrier has a unique SMS gateway hostname.
This method is completely free and can be useful in a variety of ways.

Video: https://youtu.be/hKxtMaa2hwQ
Turn on: https://myaccount.google.com/lesssecureapps
"""

import asyncio
import re
from email.message import EmailMessage
from typing import Tuple

import aiosmtplib

HOST = "smtp.gmail.com"
# https://kb.sandisk.com/app/answers/detail/a_id/17056/~/list-of-mobile-carrier-gateway-addresses
# https://www.gmass.co/blog/send-text-from-gmail/
CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
}


async def send_txt(*args: str) -> Tuple[dict, str]:
    num, carrier, email, pword, msg, subj = args
    num = str(num)
    to_email = CARRIER_MAP[carrier]

    # build message
    message = EmailMessage()
    message["From"] = email
    message["To"] = f"{num}@{to_email}"
    message["Subject"] = subj
    message.set_content(msg)

    # send
    send_kws = dict(username=email, password=pword, hostname=HOST, port=587, start_tls=True)
    res = await aiosmtplib.send(message, **send_kws)  # type: ignore
    msg = "failed" if not re.search(r"\sOK\s", res[1]) else "succeeded"
    print(msg)
    return res


if __name__ == "__main__":
    _num = "999999999"
    _carrier = "verizon"
    _email = "user@gmail.com"
    _pword = "pword"
    _msg = "Dummy msg"
    _subj = "Dummy subj"
    coro = send_txt(_num, _carrier, _email, _pword, _msg, _subj)
    asyncio.run(coro)
