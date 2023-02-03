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


# import os
from typing import Union

from .upload import upload_dir_contents
from .uploadgram import Uploadgram


async def _main(
    dir_path: str,
    destination_chat: Union[str, int],
    delete_on_success: bool = False,
    thumbnail_file: str = None,
    force_document: bool = False,
    custom_caption: str = None,
    console_progress: bool = False,
    sleep_timeout: int = 10,
):
    uploadgram = Uploadgram()
    await uploadgram.start()

    destination_chat = (await uploadgram.get_chat(destination_chat)).id

    # sent a message to verify write permission in the "destination_chat"
    status_message = await uploadgram.send_message(
        chat_id=destination_chat, text="."
    )

    # get the max tg file_size that is allowed for this account
    tg_max_file_size = 4194304000 if uploadgram.me.is_premium else 2097152000

    await upload_dir_contents(
        tg_max_file_size,
        dir_path,
        delete_on_success,
        thumbnail_file,
        force_document,
        custom_caption,
        status_message,
        console_progress,
        sleep_timeout,
    )

    await status_message.delete()
    await uploadgram.stop()


def main():
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        prog="UploadGram", description="Upload to Telegram, from the Terminal."
    )
    parser.add_argument(
        "chat_id",
        type=str,
        help="chat id for this bot to send the message to",
    )
    parser.add_argument(
        "dir_path",
        type=str,
        help="enter path to upload to Telegram",
    )
    parser.add_argument(
        "-d",
        "--delete-on-success",
        action="store_true",
        help="delete file on successful upload",
        required=False,
    )
    parser.add_argument(
        "-fd",
        "--force-doc",
        action="store_true",
        help="force uploading as documents",
        required=False,
    )
    parser.add_argument(
        "-t",
        "--thumb",
        nargs="?",
        type=str,
        help="thumbnail for the upload",
        default=None,
        required=False,
    )
    parser.add_argument(
        "-c",
        "--caption",
        nargs="?",
        type=str,
        help="custom caption for the files, instead of file_name as caption",
        default=None,
        required=False,
    )
    parser.add_argument(
        "-p",
        "--progress",
        action="store_true",
        help="show upload progress in terminal",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--sleep",
        nargs="?",
        type=int,
        default=10,
        help="sleep timeout in seconds",
        required=False,
    )
    args = parser.parse_args()

    destination_chat = args.chat_id
    if (destination_chat.isnumeric() or destination_chat.startswith("-100")):
        destination_chat = int(destination_chat)
    """
    dir_path = args.dir_path
    if not dir_path:
        dir_path = input("enter path to upload to Telegram: ")
    while not os.path.exists(dir_path):
        print(os.listdir(os.getcwd()))
        dir_path = input("please enter valid path to upload to Telegram: ")
    dir_path = os.path.abspath(dir_path)
    """

    asyncio.run(
        _main(
            dir_path=args.dir_path,
            destination_chat=destination_chat,
            delete_on_success=args.delete_on_success,
            thumbnail_file=args.thumb,
            force_document=args.force_doc,
            custom_caption=args.caption,
            console_progress=args.progress,
            sleep_timeout=args.sleep,
        )
    )


if __name__ == "__main__":
    main()
