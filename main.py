import asyncio
import logging
import sys

from scripts.api import load_api as LLM_API
from scripts.tools import custom_filter, TOKEN, ERROR_MSG

from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ParseMode
from aiogram.types import Message

# Load APIs
SHOTO = LLM_API()
dp = Dispatcher()

@dp.message(F.func(lambda message: custom_filter(message)))
async def message_handler(message: Message, bot: Bot) -> None:
    """ Main handler """
    try:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            ans, stick = await SHOTO.get_response(message)

            msg = await bot.send_message(message.chat.id, ans, reply_to_message_id=message.message_id)
            if stick: await bot.send_sticker(message.chat.id, FSInputFile(stick), reply_to_message_id=msg.message_id)
    except Exception as e:
        await bot.send_message(message.chat.id, ERROR_MSG.format(error=e), reply_to_message_id=message.message_id)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)
    logging.info("Bot started polling.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())