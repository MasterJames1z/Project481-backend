import bcrypt

from models.user import User
from sqlalchemy import event
from .database import db


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(User(username='jamesza500', password=bcrypt.hashpw('jamesza500'.encode('utf-8'),bcrypt.gensalt(10)),anime_id=None))
    db.session.commit()