import asyncio
from telethon import TelegramClient, functions, types
from telethon.errors import ChatAdminRequiredError
import time
import random
from datetime import datetime

api_id, api_hash = input("Введите API: "), input("Введите HASH: ")

client = TelegramClient("programm", api_id, api_hash)

def get_random_reaction():
    reactions = ['❤', '🔥', '👍']
    return random.choice(reactions)

class Statistics:
    def __init__(self):
        self.total_stories_viewed = 0
        self.total_reactions_sent = 0
        self.session_start_time = datetime.now()
        self.last_stat_time = datetime.now()
        self.stories_by_dialog = {}
        self.reactions_by_type = {'❤': 0, '🔥': 0, '👍': 0}
    
    def add_story_view(self, dialog_title):
        self.total_stories_viewed += 1
        if dialog_title in self.stories_by_dialog:
            self.stories_by_dialog[dialog_title] += 1
        else:
            self.stories_by_dialog[dialog_title] = 1
    
    def add_reaction(self, reaction_type):
        self.total_reactions_sent += 1
        if reaction_type in self.reactions_by_type:
            self.reactions_by_type[reaction_type] += 1
    
    def print_detailed_stats(self):
        current_time = datetime.now()
        session_duration = current_time - self.session_start_time
        stat_interval = current_time - self.last_stat_time
        
        print("\n" + "="*50)
        print("ДЕТАЛЬНАЯ СТАТИСТИКА")
        print("="*50)
        print(f"Общее время работы: {session_duration}")
        print(f"Интервал статистики: {stat_interval}")
        print(f"Всего просмотрено историй: {self.total_stories_viewed}")
        print(f"Всего отправлено реакций: {self.total_reactions_sent}")
        
        if self.total_stories_viewed > 0:
            efficiency = (self.total_reactions_sent / self.total_stories_viewed) * 100
            print(f"Эффективность: {efficiency:.1f}%")
        
        print("\nРеакции по типам:")
        for reaction_type, count in self.reactions_by_type.items():
            print(f"  {reaction_type}: {count}")
        
        print("\nИстории по диалогам:")
        for dialog, count in self.stories_by_dialog.items():
            print(f"  {dialog}: {count}")
        
        print("="*50)
        self.last_stat_time = current_time

stats = Statistics()

async def process_stories():
    session_stories = 0
    session_reactions = 0
    
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

                            stories_count = 0
                            try:
                                stories = await client(functions.stories.GetPeerStoriesRequest(peer=user))
                                stories_count = len(stories.stories.stories) if stories.stories else 0
                            except:
                                stories_count = 0

                            if max_id_value and max_id_value > 0:
                                await client(functions.stories.ReadStoriesRequest(
                                    peer=user,
                                    max_id=max_id_value
                                ))
                                stats.add_story_view(dialog.title)
                                session_stories += 1
                                print(f"Прочитана история: {user.id}")

                                if stories_count >= 2:
                                    try:
                                        stories_list = await client(functions.stories.GetPeerStoriesRequest(peer=user))
                                        if stories_list.stories and len(stories_list.stories.stories) >= 2:
                                            second_story_id = stories_list.stories.stories[1].id
                                            reaction_emoji = get_random_reaction()
                                            await client(functions.stories.SendReactionRequest(
                                                peer=user,
                                                story_id=second_story_id,
                                                reaction=types.ReactionEmoji(emoticon=reaction_emoji)
                                            ))
                                            stats.add_reaction(reaction_emoji)
                                            session_reactions += 1
                                            print(f"Отправлена реакция {reaction_emoji} на вторую историю пользователя {user.id}")
                                    except Exception as e:
                                        print(f'Ошибка при отправке реакции: {e}')
                            else:
                                await client(functions.stories.ReadStoriesRequest(
                                    peer=user
                                ))
                                stats.add_story_view(dialog.title)
                                session_stories += 1
                                print(f"Прочитана история: {user.id}")

                                if stories_count == 1:
                                    try:
                                        stories_list = await client(functions.stories.GetPeerStoriesRequest(peer=user))
                                        if stories_list.stories and len(stories_list.stories.stories) == 1:
                                            first_story_id = stories_list.stories.stories[0].id
                                            reaction_emoji = get_random_reaction()
                                            await client(functions.stories.SendReactionRequest(
                                                peer=user,
                                                story_id=first_story_id,
                                                reaction=types.ReactionEmoji(emoticon=reaction_emoji)
                                            ))
                                            stats.add_reaction(reaction_emoji)
                                            session_reactions += 1
                                            print(f"Отправлена реакция {reaction_emoji} на единственную историю пользователя {user.id}")
                                    except Exception as e:
                                        print(f'Ошибка при отправке реакции: {e}')

                            time.sleep(5)
                        except Exception as e:
                            print(f'Ошибка при просмотре историй пользователя {user.id}: {e}')
            except ChatAdminRequiredError:
                print(f'Недостаточно прав для получения участников из: {dialog.title}. Пропуск...')
            except Exception as e:
                print(f'Ошибка при получении участников из: {dialog.title}. {e}')
    
    print(f'[СЕССИЯ] Просмотрено историй: {session_stories} | Отправлено реакций: {session_reactions}')
    stats.print_detailed_stats()

async def main():
    try:
        async with client:
            await client.start()
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n=== Цикл обработки #{cycle_count} ===")
                await process_stories()
                print(f"\nОжидание перед следующим циклом...")
                await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("\nФинальная статистика:")
        stats.print_detailed_stats()
        print("Программа прервана пользователем.")

if __name__ == "__main__":
    asyncio.run(main())
