import asyncio
from telethon import TelegramClient, functions, types
from telethon.errors import ChatAdminRequiredError, SessionPasswordNeededError
import time
import random
from datetime import datetime
import json
import os


class AccountManager:
    def __init__(self):
        self.accounts = []
        self.current_account_index = 0

    def load_accounts_from_file(self, filename="accounts.txt"):
        """Загрузка аккаунтов из файла"""
        if not os.path.exists(filename):
            return False

        self.accounts = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 2:
                        account = {
                            'api_id': parts[0].strip(),
                            'api_hash': parts[1].strip(),
                            'phone': parts[2].strip() if len(parts) > 2 else '',
                            'proxy': json.loads(parts[3]) if len(parts) > 3 and parts[3] else None
                        }
                        self.accounts.append(account)
        return len(self.accounts) > 0

    def get_next_account(self):
        """Получение следующего аккаунта для ротации"""
        if not self.accounts:
            return None

        account = self.accounts[self.current_account_index]
        self.current_account_index = (self.current_account_index + 1) % len(self.accounts)
        return account

    def create_client(self, account):
        """Создание клиента Telegram с учетом прокси"""
        if account.get('proxy'):
            proxy_data = account['proxy']
            proxy = (proxy_data['server'], proxy_data['port'], proxy_data.get('secret'))
            return TelegramClient(f"sessions/{account['phone']}",
                                  account['api_id'],
                                  account['api_hash'],
                                  proxy=proxy)
        else:
            return TelegramClient(f"sessions/{account['phone']}",
                                  account['api_id'],
                                  account['api_hash'])


def get_random_reaction():
    reactions = ['❤', '🔥', '👍']
    return random.choice(reactions)


class AdvancedStatistics:
    def __init__(self):
        self.total_stories_viewed = 0
        self.total_reactions_sent = 0
        self.new_subscribers = 0
        self.session_start_time = datetime.now()
        self.last_stat_time = datetime.now()
        self.stories_by_dialog = {}
        self.reactions_by_type = {'❤': 0, '🔥': 0, '👍': 0}
        self.initial_subscribers_count = None

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

    def set_initial_subscribers(self, count):
        """Установить начальное количество подписчиков"""
        if self.initial_subscribers_count is None:
            self.initial_subscribers_count = count

    def update_subscribers(self, current_count):
        """Обновить статистику подписчиков"""
        if self.initial_subscribers_count is not None and current_count > self.initial_subscribers_count:
            self.new_subscribers = current_count - self.initial_subscribers_count

    def print_real_time_stats(self):
        """Вывод статистики в реальном времени"""
        current_time = datetime.now()
        session_duration = current_time - self.session_start_time

        print(
            f"\n📊 [РЕАЛЬНОЕ ВРЕМЯ] | ⏱️ {session_duration} | 👀 {self.total_stories_viewed} | ❤️ {self.total_reactions_sent} | 📈 +{self.new_subscribers}")

    def print_detailed_stats(self):
        current_time = datetime.now()
        session_duration = current_time - self.session_start_time
        stat_interval = current_time - self.last_stat_time

        print("\n" + "=" * 60)
        print("📈 ДЕТАЛЬНАЯ СТАТИСТИКА")
        print("=" * 60)
        print(f"🕐 Общее время работы: {session_duration}")
        print(f"⏰ Интервал статистики: {stat_interval}")
        print(f"👀 Всего просмотрено историй: {self.total_stories_viewed}")
        print(f"❤️ Всего отправлено реакций: {self.total_reactions_sent}")
        print(f"📈 Новых подписчиков: +{self.new_subscribers}")

        if self.total_stories_viewed > 0:
            efficiency = (self.total_reactions_sent / self.total_stories_viewed) * 100
            print(f"⚡ Эффективность: {efficiency:.1f}%")

        print("\n🎭 Реакции по типам:")
        for reaction_type, count in self.reactions_by_type.items():
            percentage = (count / self.total_reactions_sent * 100) if self.total_reactions_sent > 0 else 0
            print(f"  {reaction_type}: {count} ({percentage:.1f}%)")

        print("\n💬 Истории по диалогам:")
        for dialog, count in self.stories_by_dialog.items():
            percentage = (count / self.total_stories_viewed * 100) if self.total_stories_viewed > 0 else 0
            print(f"  {dialog}: {count} ({percentage:.1f}%)")

        print("=" * 60)
        self.last_stat_time = current_time


async def get_subscribers_count(client, username):
    """Получить количество подписчиков канала"""
    try:
        entity = await client.get_entity(username)
        if hasattr(entity, 'participants_count'):
            return entity.participants_count
    except Exception as e:
        print(f"Ошибка при получении подписчиков {username}: {e}")
    return 0


async def process_stories_with_client(client, stats, account_info):
    """Обработка историй для конкретного клиента"""
    session_stories = 0
    session_reactions = 0

    print(f"\n🔧 Аккаунт в работе: {account_info.get('phone', 'Unknown')}")

    # Получение начального количества подписчиков (если указан username)
    my_username = None
    try:
        me = await client.get_me()
        if me.username:
            my_username = me.username
            initial_subs = await get_subscribers_count(client, me.username)
            stats.set_initial_subscribers(initial_subs)
            print(f"👥 Начальное количество подписчиков: {initial_subs}")
    except Exception as e:
        print(f"Ошибка при получении информации об аккаунте: {e}")

    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            print(f'\n💬 Обрабатывается диалог: {dialog.title}')
            try:
                async for user in client.iter_participants(dialog.entity):
                    if user.stories_unavailable or user.stories_hidden:
                        continue

                    if user.stories_max_id:
                        try:
                            print(f'👤 Идентификатор пользователя: {user.id}')

                            # Получаем информацию об историях пользователя
                            stories_count = 0
                            try:
                                stories = await client(functions.stories.GetPeerStoriesRequest(peer=user))
                                stories_count = len(stories.stories.stories) if stories.stories else 0
                                print(f'📖 Найдено историй: {stories_count}')
                            except Exception as e:
                                print(f'⚠️ Ошибка при получении историй пользователя {user.id}: {e}')
                                continue

                            # Определяем max_id_value
                            if hasattr(user, 'stories_max_id') and isinstance(user.stories_max_id, int):
                                max_id_value = user.stories_max_id
                            else:
                                max_id_value = None

                            # Просмотр историй
                            if max_id_value and max_id_value > 0:
                                await client(functions.stories.ReadStoriesRequest(
                                    peer=user,
                                    max_id=max_id_value
                                ))
                            else:
                                await client(functions.stories.ReadStoriesRequest(peer=user))

                            stats.add_story_view(dialog.title)
                            session_stories += 1
                            print(f"✅ Прочитана история: {user.id}")

                            # Логика отправки реакций
                            if stories_count >= 2:
                                # Для 2+ историй: реакция на вторую
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
                                        print(
                                            f"🎯 Отправлена реакция {reaction_emoji} на ВТОРУЮ историю пользователя {user.id}")
                                except Exception as e:
                                    print(f'❌ Ошибка при отправке реакции: {e}')

                            elif stories_count == 1:
                                # Для одной истории: реакция на первую
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
                                        print(
                                            f"🎯 Отправлена реакция {reaction_emoji} на ЕДИНСТВЕННУЮ историю пользователя {user.id}")
                                except Exception as e:
                                    print(f'❌ Ошибка при отправке реакции: {e}')

                            # Случайная задержка между 3-7 секунд
                            await asyncio.sleep(random.uniform(3, 7))

                            # Вывод статистики в реальном времени каждые 10 действий
                            if (session_stories + session_reactions) % 10 == 0:
                                stats.print_real_time_stats()

                        except Exception as e:
                            print(f'❌ Ошибка при просмотре историй пользователя {user.id}: {e}')

            except ChatAdminRequiredError:
                print(f'🚫 Недостаточно прав для получения участников из: {dialog.title}. Пропуск...')
            except Exception as e:
                print(f'❌ Ошибка при получении участников из: {dialog.title}. {e}')

    # Обновление статистики подписчиков в конце сессии
    if my_username:
        current_subs = await get_subscribers_count(client, my_username)
        stats.update_subscribers(current_subs)

    print(f'\n✅ [СЕССИЯ ЗАВЕРШЕНА] Просмотрено историй: {session_stories} | Отправлено реакций: {session_reactions}')
    return session_stories, session_reactions


async def main():
    # Создаем папку для сессий если её нет
    os.makedirs("sessions", exist_ok=True)

    account_manager = AccountManager()
    stats = AdvancedStatistics()

    # Попытка загрузить аккаунты из файла
    if account_manager.load_accounts_from_file():
        print(f"✅ Загружено {len(account_manager.accounts)} аккаунтов из файла")
        multi_account = True
    else:
        print("⚠️ Файл accounts.txt не найден, используется ручной ввод")
        multi_account = False

    cycle_count = 0

    try:
        while True:
            cycle_count += 1

            if multi_account:
                # Мультиаккаунтный режим
                account = account_manager.get_next_account()
                client = account_manager.create_client(account)

                try:
                    async with client:
                        await client.start(phone=account.get('phone', ''))
                        print(f"\n🔄 Цикл обработки #{cycle_count} | Аккаунт: {account.get('phone', 'Unknown')}")
                        await process_stories_with_client(client, stats, account)

                except SessionPasswordNeededError:
                    print(f"🔐 Для аккаунта {account.get('phone')} требуется двухфакторная аутентификация. Пропускаем.")
                except Exception as e:
                    print(f"❌ Ошибка с аккаунтом {account.get('phone')}: {e}")

            else:
                # Одноаккаунтный режим (оригинальный)
                api_id = input("Введите API ID: ").strip()
                api_hash = input("Введите API Hash: ").strip()

                client = TelegramClient("sessions/main_session", api_id, api_hash)

                async with client:
                    await client.start()
                    print(f"\n🔄 Цикл обработки #{cycle_count}")
                    await process_stories_with_client(client, stats, {'phone': 'main_account'})
                    break  # Для одного аккаунта не бесконечный цикл

            print(f"\n⏳ Ожидание перед следующим циклом...")
            stats.print_detailed_stats()
            await asyncio.sleep(random.uniform(10, 30))  # Случайная задержка

    except KeyboardInterrupt:
        print("\n\n🛑 Финальная статистика:")
        stats.print_detailed_stats()
        print("Программа прервана пользователем.")


if __name__ == "__main__":
    asyncio.run(main())