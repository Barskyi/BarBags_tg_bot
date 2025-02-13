from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UserAction


class StatsManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_general_stats(self) -> dict:
        """Отримання загальної статистики"""
        # Унікальні користувачі
        unique_users = select(func.count(func.distinct(UserAction.user_id)))

        # Загальна кількість дій
        total_actions = select(func.count(UserAction.id))

        # Дії за останні 24 години
        day_ago = datetime.utcnow() - timedelta(days=1)
        actions_24h = select(func.count(UserAction.id)).where(UserAction.created_at > day_ago)

        results = await self.session.execute(
            select(
                (await self.session.execute(unique_users)).scalar(),
                (await self.session.execute(total_actions)).scalar(),
                (await self.session.execute(actions_24h)).scalar(),
            )
        )

        users_count, actions_count, actions_24h_count = results.first()

        return {
            "total_users": users_count or 0,
            "total_actions": actions_count or 0,
            "actions_24h": actions_24h_count or 0
        }

    async def get_popular_actions(self, limit: int = 5) -> list:
        """Отримання найпопулярніших дій"""
        query = (
            select(
                UserAction.button_name,
                func.count(UserAction.id).label('count')
            )
            .group_by(UserAction.button_name)
            .order_by(func.count(UserAction.id).desc())
            .limit(limit)
        )

        try:
            result = await self.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error in get_popular_actions: {e}")
            return []