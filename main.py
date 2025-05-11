import asyncio
from telethon import TelegramClient, functions
from telethon.errors import ChatAdminRequiredError
import time

api_id, api_hash = input("Введите API: "), input("Введите HASH: ")

client = TelegramClient("programm", api_id, api_hash)


async def process_stories():
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            print(f'Обрабатывается диалог: {dialog.title}')
            try:
                async for user in client.iter_participants(dialog.entity):
                    if user.stories_unavailable or user.stories_hidden:
                        continue
                    if user.stories_max_id:
                        try:
                            print(f'Идентификатор пользователя: {user.id}')


                            if hasattr(user, 'stories_max_id') and isinstance(user.stories_max_id, int):
                                max_id_value = user.stories_max_id
                                print(f'Значение max_id для пользователя {user.id}: {max_id_value}')
                            else:
                                print(f'Пользователь {user.id} не имеет параметра stories_max_id или он некорректен.')
                                max_id_value = None


                            if max_id_value and max_id_value > 0:
                                stories = await client(functions.stories.ReadStoriesRequest(
                                    peer=user,
                                    max_id=max_id_value

                                ))
                                print(f"Прочитана история: {user.id}")
                            else:
                                stories = await client(functions.stories.ReadStoriesRequest(
                                    peer=user
                                ))
                                print(f"Прочитана история: {user.id}")


                            print(f'Объект stories: {stories}')
                            time.sleep(5)
                        except Exception as e:
                            print(f'Ошибка при просмотре историй пользователя {user.id}: {e}')
            except ChatAdminRequiredError:
                print(f'Недостаточно прав для получения участников из: {dialog.title}. Пропуск...')
            except Exception as e:
                print(f'Ошибка при получении участников из: {dialog.title}. {e}')

async def main():
    try:
        async with client:
            await client.start()
            while True:
                await process_stories()
                print()
                await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("Программа прервана пользователем.")

if __name__ == "__main__":
    asyncio.run(main())
