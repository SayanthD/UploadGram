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


import logging
from pyrogram import Client, __version__
from pyrogram.enums import ParseMode, ClientPlatform
from .config import get_config

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Uploadgram(Client):
    """
    A robust, scalable Telegram client based on Pyrogram for Uploadgram.
    """

    def __init__(self):
        try:
            api_id = int(get_config("UG_TG_APP_ID", 0))
            api_hash = get_config("UG_TG_API_HASH", "")
            sleep_threshold = int(get_config("UG_TG_ST", 10))

            if not api_id or not api_hash:
                raise ValueError("API credentials (UG_TG_APP_ID, UG_TG_API_HASH) are required.")

            super().__init__(
                name="UploadGram",
                api_id=api_id,
                api_hash=api_hash,
                parse_mode=ParseMode.HTML,
                sleep_threshold=sleep_threshold,
                workers=10,
                max_concurrent_transmissions=4,
                no_updates=True,
                device_model="Samsung SM-G998B",
                app_version="8.4.1 (2522)",
                system_version="SDK 31",
                lang_code="en",
                client_platform=ClientPlatform.ANDROID,
            )

            logging.info("Uploadgram Client initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing Uploadgram Client: {e}")
            raise

    async def start(self):
        """
        Starts the client and logs successful startup with user details.
        """
        try:
            await super().start()
            if not self.me:
                raise RuntimeError("Failed to fetch bot details. Ensure API credentials are correct.")

            logging.info(f"Client started: @{self.me.username} (Pyrogram v{__version__})")
        except Exception as e:
            logging.error(f"Failed to start Uploadgram Client: {e}")
            raise
        finally:
            logging.info("Client startup attempt complete.")

    async def stop(self):
        """
        Stops the client gracefully and logs the shutdown status.
        """
        try:
            await super().stop()
            logging.info("Uploadgram Client stopped successfully.")
        except Exception as e:
            logging.error(f"Error during client shutdown: {e}")
            raise
