"""
API Resources
"""
from flask_restful import Resource
from flask import request
from application.models import (
    Todo,
    User,
    Token,
)
from application.shared.constants import (
    JWT_ALGORITHM,
    TOKEN_EXPIRATION_TIME,
)
from application.shared.secrets import secrets
from application import sessiondb
from jose import (
    jwt,
    JWTError,
)
from sqlalchemy import and_
from datetime import datetime, timedelta
from application.shared.utils import (
    verify_password,
    get_password_hash,
)


class ServerCheck(Resource):
    def get(self):
        return {'message': 'Server is up and running'}


class TodoResource(Resource):
    def get(self, todo_id, user_id):
        """
        This function returns a todo
        parameters:
            - todo_id: str
            - user_id: str
        return:
            todo: dict
        """
        if TokenResource.authorize():
            todo = sessiondb.query(Todo).filter(
                and_(
                    Todo.id == todo_id,
                    Todo.user_id == user_id
                )
            ).first()
            return {
                "todo": todo.serialize() if todo else None
            }, 200
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401

    def post(self, user_id):
        """
        This function creates a new todo
        parameters:
            - user_id: str
        return:
            todo_id: str
        """
        if TokenResource.authorize():
            title = request.json.get('title')
            description = request.json.get('description')
            todo = Todo(title, description, user_id)
            sessiondb.add(todo)
            sessiondb.commit()
            sessiondb.refresh(todo)
            return {
                'id': todo.serialize()['id'],
                'success': True
            }, 201
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401

    def put(self, todo_id, user_id):
        """
        This function updates a todo
        parameters:
            - todo_id: str
            - user_id: str
        return:
            todo_id: str
        """
        if TokenResource.authorize():
            todo = sessiondb.query(Todo).filter(
                and_(
                    Todo.id == todo_id,
                    Todo.user_id == user_id,
                )
            ).first()
            if todo:
                todo.title = request.json.get('title')
                todo.description = request.json.get('description')
                sessiondb.commit()
                return {
                    'id': todo.serialize()['id'],
                    'success': True
                }, 200
            return {
                'id': todo_id,
                'success': False
            }, 404
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401

    def delete(self, todo_id, user_id):
        """
        This function deletes a todo
        parameters:
            - todo_id: str
            - user_id: str
        return:
            todo_id: str
        """
        if TokenResource.authorize():
            todo = sessiondb.query(Todo).filter(
                and_(
                    Todo.id == todo_id,
                    Todo.user_id == user_id,
                )
            ).first()
            if todo:
                sessiondb.delete(todo)
                sessiondb.commit()
                return {
                    'id': todo_id,
                    'success': True
                }, 200
            return {
                'id': todo_id,
                'success': False
            }, 404
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401


class TodoListResource(Resource):
    def get(self, user_id):
        """
        This function returns all todos
        parameters:
            - user_id: str
        return:
            todos: list[dict]
        """
        if TokenResource.authorize():
            return {
                'todos': [todo.serialize() for todo in sessiondb.query(Todo).filter(Todo.user_id == user_id).all()]
            }
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401


class UserResource(Resource):
    def get(self, user_id):
        """
        This function returns a user
        parameters:
            - user_id: str
        return:
            user: dict
        """
        if TokenResource.authorize():
            user = sessiondb.query(User).filter(User.id == user_id).first()
            return {
                "user": user.serialize() if user else None
            }, 200
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401

    def post(self):
        """
        This function creates a new user
        parameters:
            - name: str
            - email: str
            - password: str
        return:
            user_id: str
        """
        name = request.json.get('name').title()
        email = request.json.get('email')
        password = get_password_hash(request.json.get('password'))
        user = sessiondb.query(User).filter(User.email == email).first()
        if user:
            return {
                'success': False,
                'message': 'User already exists'
            }, 409

        user = User(name, email, password)
        sessiondb.add(user)
        sessiondb.commit()
        sessiondb.refresh(user)
        return {
            'id': user.serialize()['id'],
            'success': True,
            'message': 'User created'
        }

    def put(self, user_id):
        """
        This function updates a user
        parameters:
            - user_id: str
            - name: str
            - email: str
            - password: str
        return:
            user_id: str
        """
        if TokenResource.authorize():
            user = sessiondb.query(User).filter(User.id == user_id).first()
            if user:
                user.name = request.json.get(
                    'name').title() if request.json.get('name') else user.name
                user.email = request.json.get(
                    'email') if request.json.get('email') else user.email
                user.password = request.json.get('password') if request.json.get(
                    'password') else user.password
                sessiondb.commit()
                return {
                    'id': user.serialize()['id'],
                    'success': True,
                    'message': 'User updated'
                }, 200
            return {
                'id': user_id,
                'success': False,
                'message': 'User not found'
            }, 404
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401

    def delete(self, user_id):
        """
        This function deletes a user
        parameters:
            - user_id: str
        return:
            user_id: str
        """
        if TokenResource.authorize():
            user = sessiondb.query(User).filter(User.id == user_id).first()
            if user:
                sessiondb.delete(user)
                sessiondb.commit()
                return {
                    'id': user_id,
                    'success': True
                }, 200
            return {
                'id': user_id,
                'success': False,
                'message': 'User not found'
            }, 404
        return {
            'success': False,
            'message': 'Unauthorized',
        }, 401


class TokenResource(Resource):
    def post(self):
        """
        This function creates a new token
        parameters:
            - email: str
            - password: str
        return:
            token: str
            token_type: str
        """
        email = request.json.get('email')
        password = request.json.get('password')
        user = sessiondb.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password):
            to_encode = {
                "user_id": str(user.id),
            }
            access_token = jwt.encode(
                to_encode, secrets['secret_key'], algorithm=JWT_ALGORITHM
            )

            token = Token(
                user_id=user.id,
                token=access_token,
                expiration_time=datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_TIME)
            )
            sessiondb.add(token)
            sessiondb.commit()
            return {
                'token': access_token,
                'token_type': 'bearer',
                'success': True,
                'message': 'Token generated'
            }, 200
        return {
            'success': False,
            'message': 'Invalid email or password'
        }, 401

    @classmethod
    def authorize(self):
        """
        This function authorizes a user
        parameters:
            - token: str
        return:
            - True: bool if user is authorized
            - False: bool if user is not authorized
        """
        try:
            token = request.headers.get('Authorization')
            if token is None:
                return False
            else:
                token = token.split(' ')[1]

            payload = jwt.decode(
                token, secrets['secret_key'], algorithms=JWT_ALGORITHM)
            user_id = payload.get('user_id')
            access_token = sessiondb.query(Token).filter(
                and_(
                    Token.user_id == user_id,
                    Token.token == token,
                    Token.expiration_time > datetime.utcnow()
                )
            ).first()
            if access_token is None:
                return False
            return True
        except JWTError:
            return False
