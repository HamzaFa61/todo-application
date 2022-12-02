"""
Database models
"""
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import (
    datetime,
    timedelta,
)
from application.shared.constants import TOKEN_EXPIRATION_TIME
import uuid

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'user.id', ondelete="cascade"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, title: str = None, description: str = None, user_id: str = None):
        self.title = title
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<Todo %r>' % self.title

    def serialize(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'updated_at': str(self.updated_at),
            'created_at': str(self.created_at)
        }


class User(Base):
    __tablename__ = 'user'

    id = id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, name: str = None, email: str = None, password: str = None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'updated_at': str(self.updated_at),
            'created_at': str(self.created_at)
        }


class Token(Base):
    __tablename__ = 'token'

    id = id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'user.id', ondelete="cascade"), nullable=False)
    token = Column(String(255), nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, user_id: str = None, token: str = None, expiration_time: datetime = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_TIME)):
        self.user_id = user_id
        self.token = token
        self.expiration_time = expiration_time
