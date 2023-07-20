import time

from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest

import ggl
from ggl import SearchResult
import asyncio
from ggl import SearchGroup


async def main():
    api_id = 28027917
    api_hash = '382bb3f2583d794954ebe72e03d56db6'
    client = TelegramClient('clients_scraper', api_id, api_hash)
    await client.start()
    await client.connect()
    print('Connected')
    while True:
        dialogs = await client.get_dialogs()
        print('Getted Dialogs')
        chats: list[SearchGroup] = ggl.get_chats()
        keywords: list[str] = ggl.get_keywords()
        print('Readed chats')
        for chat in chats:
            # Adding new position
            chat.last_update = int(time.time())
            if chat.chat_id == '':
                print('Adding new Chat')
                data = await client(ImportChatInviteRequest(chat.link.split('+')[1]))
                chat.name = data.chats[0].title
                chat.chat_id = data.chats[0].id
                dialogs = await client.get_dialogs()

            # Finding dialog
            print('Finding dialog')
            for dialog in dialogs:
                if dialog.name == chat.name:
                    break
            print('Reading messages')
            async for message in client.iter_messages(dialog):  # Reading messages
                try:
                    message_time = message.date.timestamp()
                    if chat.last_update == '':
                        chat.last_update = int(time.time() - 60 * 60 * 24 * 90)
                    if int(message_time) < chat.last_update:
                        break
                    message_text = message.message
                    keyword_contains = False
                    # Trying to find keywords
                    for keyword in keywords:
                        if keyword.lower() in message_text.lower():
                            keyword_contains = True

                    if keyword_contains:
                        print('Keyword found!')
                        user_id = message.from_id.user_id
                        # Getting participant
                        print('Getting participant')
                        participant = await client.get_entity(int(user_id))
                        print(participant)
                        # Writing result
                        print('Writing result')
                        ggl.write_result(SearchResult(chat_id=participant.id, from_group=chat.name, message_text=message_text,
                                                      message_time=str(message.date), name=participant.first_name,
                                                      surname=participant.last_name, phone=participant.phone,
                                                      username=participant.username))

                except Exception as e:
                    print(e)
            ggl.update_group_info(chat)  # Updating group information
        time.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
