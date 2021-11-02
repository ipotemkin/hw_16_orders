from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from data import users, orders, offers
import prettytable
from errors import NotFoundError, ValidationError, BadRequestError
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


@app.errorhandler(BadRequestError)
def on_not_validation_error(error):
    return "Bad request error", 405


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


@app.route('/orders/')
def get_all_orders():
    return get_all_json('orders')


@app.route('/orders/<int:uid>')
def get_order_by_id(uid: int):
    return get_json('orders', uid)


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
    if not (user := User.query.get(uid)):
        raise NotFoundError
    update_user_ = request.get_json()
    if first_name := update_user_.get('first_name'):
        user.first_name = first_name
    if last_name := update_user_.get('last_name'):
        user.last_name = last_name
    if age := update_user_.get('age'):
        user.age = age
    if email := update_user_.get('email'):
        user.email = email
    if role := update_user_.get('role'):
        user.role = role
    if phone := update_user_.get('phone'):
        user.phone = phone
    db.session.add(user)
    db.session.commit()
    return get_json('users', uid)


@app.route('/users/<int:uid>', methods=['DELETE'])
def del_user(uid):
    if not (user_ := User.query.get(uid)):
        raise NotFoundError
    db.session.delete(user_)
    db.session.commit()
    return f"User: {uid} deleted", 200


@app.route('/orders/', methods=['POST'])
def add_order():
    if not (new_order := request.get_json()):
        raise BadRequestError
    print(new_order)
    order_ = Order(**new_order)
    db.session.add(order_)
    db.session.commit()
    return new_order, 201


@app.route('/orders/<int:uid>', methods=['PUT'])
def update_order(uid: int):
    if not (order := Order.query.get(uid)):
        raise NotFoundError
    update_order_ = request.get_json()
    if name := update_order_.get('name'):
        order.name = name
    if desc := update_order_.get('description'):
        order.description = desc
    if start_date := update_order_.get('start_date'):
        order.start_date = start_date
    if end_date := update_order_.get('end_date'):
        order.end_date = end_date
    if address := update_order_.get('address'):
        order.address = address
    if price := update_order_.get('price'):
        order.price = price
    if customer_id := update_order_.get('customer_id'):
        order.customer_id = customer_id
    if executor_id := update_order_.get('executor_id'):
        order.executor_id = executor_id
    db.session.add(order)
    db.session.commit()
    return get_json('orders', uid)


@app.route('/orders/<int:uid>', methods=['DELETE'])
def del_order(uid):
    if not (order_ := Order.query.get(uid)):
        raise NotFoundError
    db.session.delete(order_)
    db.session.commit()
    return f"Order: {uid} deleted", 200


@app.route('/offers/', methods=['POST'])
def add_offer():
    if not (new_offer := request.get_json()):
        raise BadRequestError
    print(new_offer)
    offer_ = Offer(**new_offer)
    db.session.add(offer_)
    db.session.commit()
    return new_offer, 201


@app.route('/offers/<int:uid>', methods=['PUT'])
def update_offer(uid: int):
    if not (offer := Offer.query.get(uid)):
        raise NotFoundError
    update_offer_ = request.get_json()
    if order_id := update_offer_.get('order_id'):
        offer.order_id = order_id
    if executor_id := update_offer_.get('executor_id'):
        offer.executor_id = executor_id
    db.session.add(offer)
    db.session.commit()
    return get_json('offers', uid)


@app.route('/offers/<int:uid>', methods=['DELETE'])
def del_offer(uid):
    if not (offer_ := Offer.query.get(uid)):
        raise NotFoundError
    db.session.delete(offer_)
    db.session.commit()
    return f"Offer: {uid} deleted", 200


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
