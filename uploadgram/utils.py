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
import math
from time import time
from typing import List, Tuple

from .config import TG_VIDEO_TYPES


def humanbytes(size: int) -> str:
    """Converts an integer size (in bytes) to a human-readable format."""
    if size < 0:
        return "Invalid size"
    if size == 0:
        return "0 B"

    # Define units
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]

    # Calculate the appropriate unit using logarithms for efficiency
    n = min(int(math.log(size, 1024)), len(units) - 1)
    
    # Perform the size conversion
    human_readable_size = size / (1024 ** n)
    
    # Return formatted result
    return f"{human_readable_size:.2f} {units[n]}"



def time_formatter(seconds: int) -> str:
    """Converts an integer representing seconds into a human-readable format."""
    if seconds < 0:
        return "Invalid time"
    if seconds == 0:
        return "0 seconds"

    # Time units in descending order
    time_units = (
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    )

    result = []
    for unit, divisor in time_units:
        value, seconds = divmod(seconds, divisor)
        if value:
            result.append(f"{value} {unit}{'s' if value > 1 else ''}")

    return " ".join(result)


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
            "-hide_banner",
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
