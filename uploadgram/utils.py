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


import asyncio
import os

from time import time
from typing import List, Tuple

from .config import TG_VIDEO_TYPES


def humanbytes(size: int) -> str:
    """converts integer to string"""
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return "NaN"
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"


def time_formatter(seconds: int) -> str:
    """converts integer to string"""
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {
        "days": (24 * 60 * 60),
        "hours": (60 * 60),
        "minutes": 60,
        "seconds": 1,
    }
    for age, divisor in r_ange_s.items():
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m} {age} "
    return result


async def run_command(shell_command: List) -> Tuple[int, int, str, str]:
    """executes a shell_command,
    and returns the stdout and stderr"""
    process = await asyncio.create_subprocess_exec(
        *shell_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    return (
        process.pid,
        process.returncode,
        stdout.decode().strip(),
        stderr.decode().strip(),
    )


async def take_screen_shot(video_file: str, output_directory: str, ttl: int):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = os.path.join(output_directory, f"{str(time())}.jpg")
    if video_file.upper().endswith(TG_VIDEO_TYPES):
        file_genertor_command = [
            "ffmpeg",
            "-ss",
            str(ttl),
            "-i",
            video_file,
            "-vframes",
            "1",
            out_put_file_name,
        ]
        # width = "90"
        await run_command(file_genertor_command)
    return out_put_file_name if os.path.lexists(out_put_file_name) else None
