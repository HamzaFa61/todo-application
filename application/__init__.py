"""
Main Application package.
"""
from flask import (
    Flask,
)
from flask_restful import Api
from sqlalchemy.ext.declarative import declarative_base
from application.settings.db_config import init_connection_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

# Database configuration
engine = init_connection_engine()
sessiondb = scoped_session(sessionmaker(bind=engine))()
Base = declarative_base()


def add_api_resources(api):
    """
    This function adds api resources to flask application
    """
    from application.resources import (
        ServerCheck,
        TodoResource,
        TodoListResource,
        UserResource,
        TokenResource,
    )
    api.add_resource(ServerCheck, '/server-check')
    api.add_resource(
        TodoResource, '/todo/<string:todo_id>/user/<string:user_id>', '/todo/user/<string:user_id>')
    api.add_resource(TodoListResource, '/todos/user/<string:user_id>')
    api.add_resource(UserResource, '/user',
                     '/user/<string:user_id>')
    api.add_resource(TokenResource, '/token')
    return None


def create_app():
    """
    this function create Flask Application
    """
    app = Flask(__name__)
    api = Api(app)
    add_api_resources(api)
    return app
