from flask_restful import Resource, abort, reqparse
from src.Models.Display.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)
import uuid, bcrypt, hashlib, base64

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help='This field cannot be blank.'
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help='This field cannot be blank.'
                    )

def hashpw(password):
    password = password.encode('utf-8')
    password = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password).digest()), bcrypt.gensalt())
    return password.decode()


def checkpw(password, hash):
    password = password.encode('utf-8')
    password = bcrypt.checkpw(base64.b64encode(hashlib.sha256(password).digest()), hash.encode())

    return password

class UserRegister(Resource):
    @jwt_required
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.get_user_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(username=data['username'], password=hashpw(data['password']))
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel.get_user_by_username(username)
        if user:
            return user.json(), 200
        abort(404, message="User {} doesn't exist".format(username))


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.get_user_by_username(data['username'])

        if user and checkpw(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
               'access_token': access_token,
               'refresh_token': refresh_token,
            }, 200

        abort(401, message='Invalid credentials')

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': new_token}, 200



