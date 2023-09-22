import random
from faker import Faker
from app.models import User, Article
from app.utils.dependencies.get_session import get_session

fake = Faker()


async def generate_random_data():
    async for session in get_session():
        async with session.begin():
            users = []
            for _ in range(random.randint(5, 10)):
                user = User(name=fake.name(), age=random.randint(18, 65))
                session.add(user)
                await session.flush()
                users.append(user)

            for user in users:
                for _ in range(random.randint(1, 5)):
                    article = Article(
                        text=fake.text(),
                        color=random.choice(['red', 'blue', 'green']),
                        owner=user
                    )
                    session.add(article)
                    await session.flush()
