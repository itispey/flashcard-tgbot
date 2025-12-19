import logging
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bot.models import Category, Collection, Flashcard, User
from bot.utils.helpers.db import SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()


def create_test_data():
    db = SessionLocal()
    try:
        logger.info("Starting to generate test data...")

        # Generate Users
        users = []
        for _ in range(5):
            user = User(
                tg_id=fake.unique.random_number(digits=10),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
            )
            db.add(user)
            users.append(user)

        db.commit()
        logger.info(f"Created {len(users)} users.")

        # Generate Categories for each user
        categories = []
        for user in users:
            for _ in range(2):
                category = Category(
                    name=fake.word().capitalize(),
                    description=fake.sentence(),
                    author_id=user.tg_id,
                    is_public=True,
                )
                db.add(category)
                categories.append(category)

        db.commit()
        logger.info(f"Created {len(categories)} categories.")

        # Generate Collections for each category
        collections = []
        for category in categories:
            for _ in range(2):
                collection = Collection(
                    name=fake.word().capitalize(), category_id=category.id
                )
                db.add(collection)
                collections.append(collection)

        db.commit()
        logger.info(f"Created {len(collections)} collections.")

        # Generate Flashcards for each collection
        flashcards_count = 0
        for collection in collections:
            for _ in range(5):
                flashcard = Flashcard(
                    term=fake.word(),
                    definition=fake.sentence(),
                    collection_id=collection.id,
                    example=fake.sentence(),
                    synonym=fake.word(),
                    antonym=fake.word(),
                )
                db.add(flashcard)
                flashcards_count += 1

        db.commit()
        logger.info(f"Created {flashcards_count} flashcards.")

        # Add Random Subscriptions
        # Randomly subscribe users to categories they don't own
        subscriptions_count = 0
        for user in users:
            # Get categories not owned by user
            available_categories = [c for c in categories if c.author_id != user.tg_id]
            if available_categories:
                # Subscribe to 1-3 random categories
                cats_to_sub = random.sample(
                    available_categories,
                    k=min(len(available_categories), random.randint(1, 3)),
                )
                for cat in cats_to_sub:
                    user.bookmarked_categories.append(cat)
                    subscriptions_count += 1

        db.commit()
        logger.info(f"Created {subscriptions_count} subscriptions.")

        logger.info("Test data generation completed successfully!")

    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError occurred: {e}")
    except Exception as e:
        db.rollback()
        logger.error(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
