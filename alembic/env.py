from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.bd.models import Base
from config import settings  # Импортируем Pydantic Settings

# Alembic Config object
config = context.config

# Настройка логирования из файла конфигурации
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для автогенерации миграций
target_metadata = Base.metadata

# Функция для получения строки подключения
def get_url():
    # Проверяем, передана ли строка подключения через аргумент `-x url`
    url = context.get_x_argument(as_dictionary=True).get("url")
    if not url:
        # Если аргумент не передан, используем Pydantic
        url = settings.DATABASE_URL_PSYCOPG2
    return url

# Режим "оффлайн"
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Режим "онлайн"
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Определяем режим миграции (оффлайн или онлайн)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
