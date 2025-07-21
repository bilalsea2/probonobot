import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.handlers import setup_routers

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize bot and dispatcher
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    bot = Bot(token=bot_token)
    storage = MemoryStorage() # Use MemoryStorage for simplicity, consider Redis for production
    dp = Dispatcher(storage=storage)

    # Register routers
    setup_routers(dp)

    # Start polling
    logger.info("Bot started polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")