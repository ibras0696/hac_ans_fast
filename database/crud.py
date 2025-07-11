import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database.db import AsyncSessionLocal
from database.models import *


class CrudUser:
    def __init__(self):
        self.session: async_sessionmaker = AsyncSessionLocal

    # 1. Добавление пользователя
    async def add_user(self,
                       username: str,
                       password_hash: str,
                       full_name: str = None,
                       is_moderator: bool = False) -> User:
        """
        Создаёт нового пользователя и сохраняет в базе.
        :param username: уникальное имя пользователя
        :param password_hash: хеш пароля
        :param full_name: полное имя (опционально)
        :param is_moderator: флаг модератора (по умолчанию False)
        :return: объект User с заполнённым id и временем регистрации
        """
        async with self.session() as session:
            try:
                user = User(
                    username=username,
                    password_hash=password_hash,
                    full_name=full_name,
                    is_moderator=is_moderator,
                )
                session.add(user)
                await session.commit()
                return user
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при добавлении пользователя: {e}")

    # 2. Получение пользователя по ID
    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()

    # 3. Получение пользователя по username
    async def get_user_by_username(self, username: str) -> User | None:
        async with self.session() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()

    # 4. Удаление пользователя по ID
    async def delete_user(self, user_id: int) -> bool:
        async with self.session() as session:
            try:
                result = await session.execute(select(User).where(User.id == user_id))
                user = result.scalar_one_or_none()
                if not user:
                    return False
                await session.delete(user)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при удалении пользователя: {e}")

    # 5. Получение списка всех пользователей
    async def list_users(self) -> list[User]:
        async with self.session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()


    async def set_moderator_status(self, username: str, is_moderator: bool) -> bool:
        """
        Обновляет статус модератора пользователя.

        :param username: ID пользователя
        :param is_moderator: новый статус модератора
        :return: True, если обновление прошло успешно, False если пользователь не найден
        """
        async with self.session() as conn:
            try:
                result = await conn.execute(select(User).where(User.username == username))
                user = result.scalar_one_or_none()
                if not user:
                    return False
                user.is_moderator = is_moderator
                await conn.commit()
                return True
            except SQLAlchemyError as e:
                await conn.rollback()
                raise Exception(f"Ошибка при обновлении статуса модератора: {e}")


class CrudActivity:
    def __init__(self):
        self.session: async_sessionmaker = AsyncSessionLocal

    # 1. Добавление новой активности
    async def add_activity(self,
                           title: str,
                           description: str,
                           category: str,
                           address: str,
                           images: str,
                           working_hours: str,
                           rating: float) -> Activity:
        """
        Создаёт новую активность.
        :param title: название
        :param description: описание
        :param category: категория (например, "спорт", "музей")
        :param address: адрес (с городом)
        :param images: ссылки или пути к картинкам
        :param working_hours: часы работы, например "10:00-20:00"
        :param rating: рейтинг (от 0 до 5)
        :return: объект Activity с ID
        """
        async with self.session() as session:
            try:
                activity = Activity(
                    title=title,
                    description=description,
                    category=category,
                    address=address,
                    images=images,
                    working_hours=working_hours,
                    rating=rating
                )
                session.add(activity)
                await session.commit()
                return activity
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при добавлении активности: {e}")

    # 2. Получение активности по ID
    async def get_activity_by_id(self, activity_id: int) -> Activity | None:
        async with self.session() as session:
            result = await session.execute(
                select(Activity).where(Activity.id == activity_id)
            )
            return result.scalar_one_or_none()

    # 3. Удаление активности по ID
    async def delete_activity(self, activity_id: int) -> bool:
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(Activity).where(Activity.id == activity_id)
                )
                activity = result.scalar_one_or_none()
                if not activity:
                    return False

                await session.delete(activity)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при удалении активности: {e}")

    # 4. Получить список всех активностей
    async def list_activities(self) -> list[Activity]:
        async with self.session() as session:
            result = await session.execute(select(Activity))
            return result.scalars().all()


    # 5. Получить активности по категории и городу
    async def list_activities_by_category(self, city: str, category: str) -> list[Activity]:
        """
        Фильтрует активности по категории и городу.
        Поиск по адресу (используется ilike для нечувствительности к регистру).
        """
        async with self.session() as session:
            result = await session.execute(
                select(Activity).where(
                    Activity.category == category,
                    Activity.address.ilike(f"%{city}%")
                )
            )
            return result.scalars().all()


class CrudPreferences:
    def __init__(self):
        self.session: async_sessionmaker = AsyncSessionLocal

    # 1. Добавить или обновить предпочтения пользователя
    async def add_or_update_preferences(self, user_id: int, mood: str, time_available: int, budget: int) -> UserPreferences:
        """
        Если у пользователя уже есть предпочтения — обновляет их,
        иначе создаёт новую запись.
        :param user_id: ID пользователя
        :param mood: настроение
        :param time_available: сколько времени доступно (в минутах/часах)
        :param budget: бюджет (в валюте)
        :return: объект UserPreferences
        """
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(UserPreferences).where(UserPreferences.user_id == user_id)
                )
                prefs = result.scalar_one_or_none()

                if prefs:
                    prefs.mood = mood
                    prefs.time_available = time_available
                    prefs.budget = budget
                else:
                    prefs = UserPreferences(
                        user_id=user_id,
                        mood=mood,
                        time_available=time_available,
                        budget=budget
                    )
                    session.add(prefs)

                await session.commit()
                return prefs
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при добавлении/обновлении предпочтений: {e}")

    # 2. Получение предпочтений пользователя по user_id
    async def get_preferences_by_user_id(self, user_id: int) -> UserPreferences | None:
        """
        Возвращает предпочтения пользователя, либо None, если не найдено.
        """
        async with self.session() as session:
            result = await session.execute(
                select(UserPreferences).where(UserPreferences.user_id == user_id)
            )
            return result.scalar_one_or_none()

    # 3. Удаление предпочтений пользователя по user_id
    async def delete_preferences(self, user_id: int) -> bool:
        """
        Удаляет предпочтения пользователя.
        Возвращает True, если удалено, False если не найдено.
        """
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(UserPreferences).where(UserPreferences.user_id == user_id)
                )
                prefs = result.scalar_one_or_none()
                if not prefs:
                    return False
                await session.delete(prefs)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при удалении предпочтений: {e}")


class CrudActivityHistory:
    """
    Работа с историей активности пользователя: записи о том,
    какие активности он выполнял и когда.
    """

    def __init__(self):
        self.session: async_sessionmaker = AsyncSessionLocal

    # 1. Добавить запись в историю активности
    async def add_activity_history(self, user_id: int, activity_id: int) -> ActivityHistory | None:
        """
        Добавляет новую запись о том, что пользователь выполнил активность.
        :param user_id: ID пользователя
        :param activity_id: ID активности
        :return: объект ActivityHistory или None при ошибке целостности
        """
        async with self.session() as session:
            try:
                history_entry = ActivityHistory(
                    user_id=user_id,
                    activity_id=activity_id,
                    completed_at=datetime.now(timezone.utc)
                )
                session.add(history_entry)
                await session.flush()
                await session.commit()
                return history_entry
            except IntegrityError:
                await session.rollback()
                return None
            except SQLAlchemyError as ex:
                await session.rollback()
                raise Exception(f"Ошибка при добавлении в activity_history: {ex}")

    # 2. Получить историю активности пользователя по user_id
    async def get_history_by_user_id(self, user_id: int) -> list[ActivityHistory]:
        """
        Возвращает список всех записей истории активности для заданного пользователя.
        :param user_id: ID пользователя
        :return: список ActivityHistory
        """
        async with self.session() as session:
            result = await session.execute(
                select(ActivityHistory).where(ActivityHistory.user_id == user_id)
            )
            return result.scalars().all()

    # 3. Удалить запись из истории активности по ID записи
    async def delete_history_entry(self, history_id: int) -> bool:
        """
        Удаляет запись истории активности по её ID.
        :param history_id: ID записи в истории активности
        :return: True если удалена, False если не найдена
        """
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(ActivityHistory).where(ActivityHistory.id == history_id)
                )
                entry = result.scalar_one_or_none()
                if not entry:
                    return False
                await session.delete(entry)
                await session.commit()
                return True
            except SQLAlchemyError as ex:
                await session.rollback()
                raise Exception(f"Ошибка при удалении записи из activity_history: {ex}")

    # 4. Получить все записи истории активности
    async def list_all_history(self) -> list[ActivityHistory]:
        """
        Возвращает список всех записей истории активности.
        """
        async with self.session() as session:
            result = await session.execute(select(ActivityHistory))
            return result.scalars().all()


class CrudRecommendation:
    """
    Класс для работы с таблицей recommendations.
    Методы для добавления, получения, обновления и удаления рекомендаций.
    """

    def __init__(self):
        self.session: async_sessionmaker = AsyncSessionLocal

    # 1. Добавление новой рекомендации
    async def add_recommendation(self, user_id: int, activity_id: int) -> Recommendation | None:
        """
        Добавляет новую рекомендацию для пользователя.
        """
        async with self.session() as conn:
            try:
                recommendation = Recommendation(
                    user_id=user_id,
                    activity_id=activity_id,
                    recommended_at=datetime.now(timezone.utc),
                    accepted=False
                )
                conn.add(recommendation)
                await conn.flush()
                await conn.commit()
                return recommendation
            except IntegrityError:
                await conn.rollback()
                return None
            except SQLAlchemyError as ex:
                await conn.rollback()
                raise Exception(f"Ошибка при добавлении рекомендации: {ex}")

    # 2. Получение списка рекомендаций пользователя
    async def get_recommendations_by_user(self, user_id: int) -> list[Recommendation]:
        """
        Возвращает список рекомендаций для пользователя по user_id.
        """
        async with self.session() as conn:
            result = await conn.execute(
                select(Recommendation).where(Recommendation.user_id == user_id)
            )
            return result.scalars().all()

    # 3. Отметить рекомендацию как принятую (accepted=True)
    async def mark_recommendation_as_accepted(self, recommendation_id: int) -> bool:
        """
        Обновляет поле accepted в True для рекомендации с данным ID.
        """
        async with self.session() as conn:
            try:
                result = await conn.execute(
                    update(Recommendation)
                    .where(Recommendation.id == recommendation_id)
                    .values(accepted=True)
                    .execution_options(synchronize_session="fetch")
                )
                if result.rowcount == 0:
                    return False
                await conn.commit()
                return True
            except SQLAlchemyError as ex:
                await conn.rollback()
                raise Exception(f"Ошибка при обновлении рекомендации: {ex}")

    # 4. Удаление рекомендации по ID
    async def delete_recommendation(self, recommendation_id: int) -> bool:
        """
        Удаляет рекомендацию по ID.
        """
        async with self.session() as conn:
            try:
                result = await conn.execute(
                    delete(Recommendation)
                    .where(Recommendation.id == recommendation_id)
                )
                if result.rowcount == 0:
                    return False
                await conn.commit()
                return True
            except SQLAlchemyError as ex:
                await conn.rollback()
                raise Exception(f"Ошибка при удалении рекомендации: {ex}")


class CrudFavorite:
    def __init__(self):
        self.session: async_sessionmaker = AsyncSessionLocal

    # 1. Добавление активности в избранное
    async def add_favorite(self, user_id: int, activity_id: int) -> Favorite:
        """
        Добавляет активность в избранное для пользователя.
        :param user_id: ID пользователя
        :param activity_id: ID активности
        :return: объект Favorite с заполнённым id и временем добавления
        """
        async with self.session() as session:
            try:
                favorite = Favorite(
                    user_id=user_id,
                    activity_id=activity_id
                )
                session.add(favorite)
                await session.commit()
                return favorite
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при добавлении в избранное: {e}")

    # 2. Получить все избранные активности пользователя
    async def get_favorites_by_user(self, user_id: int) -> list[Favorite]:
        """
        Возвращает список избранных активностей пользователя.
        :param user_id: ID пользователя
        :return: список объектов Favorite
        """
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(Favorite).where(Favorite.user_id == user_id)
                )
                favorites = result.scalars().all()
                return favorites
            except SQLAlchemyError as e:
                raise Exception(f"Ошибка при получении избранного пользователя: {e}")

    # 3. Удалить активность из избранного по ID
    async def remove_favorite(self, favorite_id: int) -> bool:
        """
        Удаляет запись избранного по её ID.
        :param favorite_id: ID записи избранного
        :return: True, если удаление успешно, иначе False
        """
        async with self.session() as session:
            try:
                favorite = await session.get(Favorite, favorite_id)
                if not favorite:
                    return False
                await session.delete(favorite)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"Ошибка при удалении из избранного: {e}")

# if __name__ == '__main__':
#     async def main2():
#         a = await CrudActivity().list_activities()
#         print(a)
#
#     asyncio.run(main2())
