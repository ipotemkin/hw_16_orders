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

    def __repr__(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'age': self.age,
                'email': self.email, 'role': self.role, 'phone': self.phone}

    def to_dict(self):
        for column in self.__table__.columns:
            print(column.name, self[column.name])

    def columns(self):
        return [column.name for column in self.__table__.columns]


USER_COLUMNS = ['id', 'first_name', 'last_name', 'age', 'email', 'role', 'phone']


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)

    def __repr__(self):
        return {'id': self.id, 'order_id': self.order_id, 'executor_id': self.executor_id}


OFFER_COLUMNS = ['id', 'order_id', 'executor_id']


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

    def __repr__(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'start_date': self.start_date,
                'end_date': self.end_date, 'address': self.address, 'price': self.price,
                'customer_id': self.customer_id, 'executor_id': self.executor_id}


ORDER_COLUMNS = ['id', 'name', 'description', 'start_date', 'end_date', 'address', 'price', 'customer_id',
                 'executor_id']


def make_str_form_dict(record: dict):
    s_lst = [str(key) + '=\'' + str(value) + '\'' for key, value in record.items()]
    return ', '.join(s_lst)


@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def on_not_found_error(error):
    return "Not found", 404


@app.errorhandler(ValidationError)
def on_not_validation_error(error):
    return "Validation error", 400


def add_column_names(column_names: list, data: list or dict):
    if not column_names or not data:
        raise NotFoundError
    results = []
    if type(data) == list:
        if len(column_names) != len(data[0].__repr__()):
            raise ValidationError
        for line_ in data:
            results_line = dict()
            for key in column_names:
                results_line[key] = line_.__repr__()[key]
            results.append(results_line)
        return results
    if len(column_names) != len(data.__repr__()):
        raise ValidationError
    return data.__repr__()


@app.route('/users/')
def get_all_users():
    res = db.engine.execute('select * from users')
    return jsonify([dict(r) for r in res])
    # return jsonify(add_column_names(USER_COLUMNS, data=User.query.all()))


@app.route('/users/<int:uid>')
def get_user_by_id(uid: int):
    return jsonify(add_column_names(USER_COLUMNS, data=User.query.get(uid)))


@app.route('/offers/')
def get_all_offers():
    return jsonify(add_column_names(OFFER_COLUMNS, data=Offer.query.all()))


@app.route('/offers/<int:uid>')
def get_offer_by_id(uid: int):
    return jsonify(add_column_names(OFFER_COLUMNS, data=Offer.query.get(uid)))


@app.route('/users/', methods=['POST'])
def add_user():
    new_user = request.get_json()
    user = User(**new_user)
    db.session.add(user)
    db.session.commit()
    return new_user, 201


@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid: int):
    user = User.query.get(uid)
    update_user_ = request.get_json()
    print(user.__repr__())
    print(update_user_)
    for field, value in update_user_.items():
        print('field =', field)
        print('value =', value)
        print('user[%s] =' % field, user.age)
        user.age = value
    db.session.add(user)
    db.session.commit()
    columns = [column.name for column in User.__table__.columns]
    return jsonify(add_column_names(columns, data=User.query.get(uid))), 200


if __name__ == '__main__':
    db.create_all()

    for line in users:
        db.session.add(User(**line))
    for line in orders:
        db.session.add(Order(**line))
    for line in offers:
        db.session.add(Offer(**line))
    db.session.commit()

    print([(key, value, type(value)) for key, value in User.__dict__.items()])
    print([column for column in User.__table__.columns])
    print([(column.name, column.type) for column in User.__table__.columns])
    user = User.query.get(1)
    print(user.columns())

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
