from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config.settings import config
import logging

logger = logging.getLogger(__name__)

logger.info("Initializing database connection...")
database_url = config.database_url
logger.info(f"Using database URL starting with: {database_url[:15]}...")

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
