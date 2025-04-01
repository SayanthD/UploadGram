#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Copyright (C) 2021 The Authors
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" progress helper """


import math
from asyncio import sleep
from time import time

from pyrogram.errors import FloodWait
from pyrogram.types import Message

from .utils import humanbytes, time_formatter


async def progress_for_pyrogram(
    current: int,
    total: int,
    message: Message,
    sfw: int,
    pbar: bool,
    ud_type: str,
):
    """Tracks upload/download progress and updates the message periodically."""

    now = time()
    if not sfw:
        return  # Prevents division errors

    elapsed = now - sfw
    if elapsed == 0:
        return  # Avoid zero-division errors

    if pbar is not None:
        pbar.update((current / total) * 1024 * 1024)
        if current == total:
            pbar.set_description("Uploaded")
        return

    if int(elapsed) % 10 != 0 and current != total:
        return  # Updates every 10 seconds or when complete

    try:
        percentage = (current / total) * 100 if total else 0
        speed = current / elapsed if elapsed > 0 else 0
        time_remaining = (total - current) / speed if speed > 0 else 0
    except ZeroDivisionError:
        percentage, speed, time_remaining = 0, 0, 0

    progress_bar = "{0}{1}".format(
        "█" * (math.floor(percentage / 5)),
        "░" * (20 - math.floor(percentage / 5)),
    )

    progress_text = (
        f"[{progress_bar}] \n"
        f"P: {round(percentage, 2)}%\n"
        f"{humanbytes(current)} of {humanbytes(total)}\n"
        f"Speed: {humanbytes(speed)}/s\n"
        f"ETA: {time_formatter(round(time_remaining)) if time_remaining else '0 seconds'}\n"
    )

    try:
        await message.edit_text(f"{ud_type}\n{progress_text}")
    except FloodWait as e:
        await sleep(e.value)  # Ensures we wait out Telegram’s flood control
    except Exception:
        pass  # Silently ignore other errors
