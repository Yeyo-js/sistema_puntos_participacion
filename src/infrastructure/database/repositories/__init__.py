"""
Repositorios de acceso a datos
"""
from .base_repository import BaseRepository
from .user_repository import UserRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
]