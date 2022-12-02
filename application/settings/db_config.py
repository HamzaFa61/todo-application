"""
Database Configurations
"""
import sqlalchemy
from application.shared.secrets import secrets
from sqlalchemy import create_engine


def init_connection_engine():
    db_config = {
        "pool_recycle": 31535999,
    }
    return init_tcp_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    engine = create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgresql+psycopg2",
            username=secrets['db_user'],
            password=secrets['db_pass'],
            host=secrets['db_host'],
            port=secrets['db_port'],
            database=secrets['db_name'],
        ),
        **db_config
    )

    return engine
