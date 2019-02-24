from src.common.db import db

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    created = db.Column(db.TIMESTAMP)
    modified = db.Column(db.TIMESTAMP)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        """ Return a directory from Model """
        return {
            'username': self.username,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_by_username(cls, username):
        """ Get CIS from database """
        return cls.query.filter_by(username=username).first()