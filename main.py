from telethon import TelegramClient, events
import asyncio
from aiogram import Dispatcher, Bot

import logging

api_id = 27363581
api_hash = 'bccb3f26df3a01ef18bc916f16b27c68'


bot = Bot('botid')
dp = Dispatcher()


# @client.on(events.NewMessage(chats=6287437487))
# async def get_newMessage(event):
#     from module import new_boundle, async_playwright

#     try:
#         for key, value in user_data.items():
#             if value["status"]:
#                 message = event.message
#                 data = message.to_dict()
#                 entities = data.get("entities", [])
                
#                 links = [entity["url"] for entity in entities if entity["_"] == "MessageEntityTextUrl"]
#                 links.pop(1)
#                 async with async_playwright() as pw:
#                     chromium = pw.chromium
#                     browser = await chromium.launch()
#                     context = await browser.new_context(proxy={"server": f"http://127.0.0.1:{user_data[key]["proxy"]}"})
#                     task = await new_boundle(links[0], user_data[key]["paste"], context, key)
#                     if task:
#                         await bot.send_message(key, f'Бандл создан на  {links[0]}, коммент "{user_data[key]["paste"]}" отправлен.')
#                     else:
#                         await bot.send_message(key, 'Бандл не создался(((')

#                     await browser.close()

#     except Exception:
#         pass

async def main():
    from app.hendlers import router
    logging.basicConfig(level=logging.INFO)
    # global client
    # for key in user_data:
    #     client = TelegramClient(f'{str(key)}', api_id=api_id, api_hash=api_hash)
    #     await client.start()
    #     await client.run_until_disconnected()
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())
