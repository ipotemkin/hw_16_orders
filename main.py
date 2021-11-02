from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from data import users, orders, offers
import prettytable
from errors import NotFoundError, ValidationError
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def on_not_found_error(error):
    return "Not found", 404


@app.errorhandler(ValidationError)
def on_not_validation_error(error):
    return "Validation error", 400


# def add_column_names(column_names: list, data: list or dict):
#     if not column_names or not data:
#         raise NotFoundError
#     results = []
#     if type(data) == list:
#         if len(column_names) != len(data[0].__repr__()):
#             raise ValidationError
#         for line_ in data:
#             results_line = dict()
#             for key in column_names:
#                 results_line[key] = line_.__repr__()[key]
#             results.append(results_line)
#         return results
#     if len(column_names) != len(data.__repr__()):
#         raise ValidationError
#     return data.__repr__()


def get_all_json(tablename: str) -> json:
    if not (res := db.engine.execute(f'select * from {tablename}')):
        raise NotFoundError
    return jsonify([dict(r) for r in res])


def get_json(tablename: str, uid: int) -> json:
    if not (res := db.engine.execute(f'select * from {tablename} where id = {uid}').first()):
        raise NotFoundError
    return jsonify(dict(res))


@app.route('/users/')
def get_all_users():
    return get_all_json('users')


@app.route('/users/<int:uid>')
def get_user_by_id(uid: int):
    return get_json('users', uid)


@app.route('/offers/')
def get_all_offers():
    return get_all_json('offers')


@app.route('/offers/<int:uid>')
def get_offer_by_id(uid: int):
    return get_json('offers', uid)


@app.route('/users/', methods=['POST'])
def add_user():
    new_user = request.get_json()
    user_ = User(**new_user)
    db.session.add(user_)
    db.session.commit()
    return new_user, 201


@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid: int):
    # user = User.query.get(uid)
    # update_user_ = request.get_json()
    # print(user.__repr__())
    # print(update_user_)
    # for field, value in update_user_.items():
    #     print('field =', field)
    #     print('value =', value)
    #     print('user[%s] =' % field, user.age)
    #     user.age = value
    # db.session.add(user)
    # db.session.commit()
    # columns = [column.name for column in User.__table__.columns]
    # return jsonify(add_column_names(columns, data=User.query.get(uid))), 200
    pass


if __name__ == '__main__':
    db.create_all()

    for line in users:
        db.session.add(User(**line))
    for line in orders:
        db.session.add(Order(**line))
    for line in offers:
        db.session.add(Offer(**line))
    db.session.commit()

    # print([(key, value, type(value)) for key, value in User.__dict__.items()])
    # print([column for column in User.__table__.columns])
    # print([(column.name, column.type) for column in User.__table__.columns])
    # user = User.query.get(1)
    # print(user.columns())

    # cursor = db.session.execute(f"SELECT * from {User.__tablename__}").cursor
    # mytable = prettytable.from_db_cursor(cursor)
    # mytable.max_width = 30
    # print(mytable)
    #
    # cursor = db.session.execute(f"SELECT * from {Order.__tablename__}").cursor
    # mytable = prettytable.from_db_cursor(cursor)
    # mytable.max_width = 30
    # print(mytable)
    #
    # cursor = db.session.execute(f"SELECT * from {Offer.__tablename__}").cursor
    # mytable = prettytable.from_db_cursor(cursor)
    # mytable.max_width = 30
    # print(mytable)

    app.run()
