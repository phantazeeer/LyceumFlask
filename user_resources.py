from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('sec_name', required=True)
parser.add_argument('country', required=True)
parser.add_argument('city', required=True)
parser.add_argument('password', required=True)
parser.add_argument('email', required=True)


parser_put = reqparse.RequestParser()
parser_put.add_argument("name", required=True)
parser_put.add_argument("surname", required=True)
parser_put.add_argument("sec_name", required=True)
parser_put.add_argument("country", required=True)
parser_put.add_argument("city", required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'surname', 'sec_name', 'country', "city", "created"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        args = parser_put.parse_args()
        user.name = args["name"]
        user.surname = args["surname"]
        user.sec_name = args["sec_name"]
        user.country = args["country"]
        user.city = args["city"]
        session.commit()
        return jsonify({'user': user.to_dict(
            only=('name', 'surname', 'sec_name', 'country', "city"))})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'surname', 'sec_name', 'country', "city", "created")) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            email=args["email"],
            hashed_pass=args["password"],
            surname=args['surname'],
            sec_name=args['sec_name'],
            country=args['country'],
            city=args['city']
        )
        user.set_password(args["password"])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})